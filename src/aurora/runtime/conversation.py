import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4

from google.adk.apps import App, ResumabilityConfig
from google.adk.events import Event
from google.adk.runners import Runner
from google.adk.sessions.sqlite_session_service import SqliteSessionService
from google.genai import types

from aurora.agents.factory import build_agents
from aurora.domain.confirmations import ConfirmationMirror
from aurora.domain.exceptions import (
    ConfirmationInvalidError,
    SessionNotFoundError,
)
from aurora.domain.identity import resolve_identity
from aurora.persistence.database import Database
from aurora.persistence.initialization import initialize_database
from aurora.persistence.models import ApartmentRecord, SessionRecord
from aurora.regulation.retriever import RegulationRetriever

APP_NAME = "aurora"
REQUEST_CONFIRMATION = "adk_request_confirmation"


@dataclass(frozen=True, slots=True)
class ActiveConfirmation:
    confirmation_id: str
    invocation_id: str
    requesting_agent: str
    action: str
    details: dict[str, str]
    payload: dict[str, object]


class ConversationService:
    def __init__(
        self,
        *,
        database_url: str,
        seed_directory: Path,
        model: str,
        api_key: str,
    ) -> None:
        self.database = Database(database_url)
        self.seed_directory = seed_directory
        self.model = model
        self.api_key = api_key
        self.session_service: SqliteSessionService | None = None
        self.runner: Runner | None = None
        self.confirmations = ConfirmationMirror(self.database)

    async def start(self) -> None:
        os.environ.setdefault("GOOGLE_API_KEY", self.api_key)
        await initialize_database(self.database, self.seed_directory)
        retriever = RegulationRetriever(self.seed_directory / "regulamento.md")
        root_agent = build_agents(
            database=self.database,
            model=self.model,
            regulation=retriever,
        )
        app = App(
            name=APP_NAME,
            root_agent=root_agent,
            resumability_config=ResumabilityConfig(is_resumable=True),
        )
        self.session_service = SqliteSessionService(self.database.url)
        self.runner = Runner(app=app, session_service=self.session_service)

    async def close(self) -> None:
        await self.database.close()

    async def create_session(self, apartment: str) -> str:
        session_id = str(uuid4())
        async with self.database.session() as domain_session:
            apartment_record = await domain_session.get(ApartmentRecord, apartment)
            if apartment_record is None:
                raise ValueError("Apartamento não encontrado.")
            domain_session.add(
                SessionRecord(session_id=session_id, apartment=apartment)
            )
        session_service = self._session_service()
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=apartment,
            session_id=session_id,
            state={},
        )
        return session_id

    async def send_message(self, session_id: str, text: str) -> dict[str, object]:
        identity = await resolve_identity(self.database, session_id)
        events = [
            event
            async for event in self._runner().run_async(
                user_id=identity.apartment,
                session_id=session_id,
                new_message=types.Content(
                    role="user",
                    parts=[types.Part(text=text)],
                ),
            )
        ]
        await self._sync_confirmations(session_id, events)
        return {
            "resposta": self._final_response(events),
            "confirmacoes_pendentes": await self.confirmations.list_pending(
                session_id
            ),
        }

    async def respond_confirmation(
        self,
        session_id: str,
        confirmation_id: str,
        confirmed: bool,
    ) -> dict[str, object]:
        identity = await resolve_identity(self.database, session_id)
        adk_session = await self._get_adk_session(
            session_id=session_id,
            apartment=identity.apartment,
        )
        active = self._active_confirmations(adk_session.events)
        pending = active.get(confirmation_id)
        if pending is None:
            raise ConfirmationInvalidError

        events = [
            event
            async for event in self._runner().run_async(
                user_id=identity.apartment,
                session_id=session_id,
                invocation_id=pending.invocation_id,
                new_message=types.Content(
                    role="user",
                    parts=[
                        types.Part(
                            function_response=types.FunctionResponse(
                                id=confirmation_id,
                                name=REQUEST_CONFIRMATION,
                                response={"confirmed": confirmed},
                            )
                        )
                    ],
                ),
            )
        ]
        status = "approved" if confirmed else "denied"
        await self.confirmations.resolve(
            confirmation_id,
            session_id,
            status,
            self._final_response(events),
        )
        return {
            "resposta": self._final_response(events),
            "confirmacoes_pendentes": await self.confirmations.list_pending(
                session_id
            ),
        }

    async def get_events(self, session_id: str) -> list[dict[str, Any]]:
        identity = await resolve_identity(self.database, session_id)
        adk_session = await self._get_adk_session(
            session_id=session_id,
            apartment=identity.apartment,
        )
        return [event.model_dump(mode="json") for event in adk_session.events]

    async def _get_adk_session(self, *, session_id: str, apartment: str):
        session = await self._session_service().get_session(
            app_name=APP_NAME,
            user_id=apartment,
            session_id=session_id,
        )
        if session is None:
            raise SessionNotFoundError
        return session

    async def _sync_confirmations(
        self,
        session_id: str,
        emitted_events: list[Event],
    ) -> None:
        del emitted_events
        identity = await resolve_identity(self.database, session_id)
        session = await self._get_adk_session(
            session_id=session_id,
            apartment=identity.apartment,
        )
        active = self._active_confirmations(session.events)
        for pending in active.values():
            await self.confirmations.upsert_pending(
                confirmation_id=pending.confirmation_id,
                session_id=session_id,
                action=pending.action,
                details=pending.details,
                payload=pending.payload,
                invocation_id=pending.invocation_id,
                requesting_agent=pending.requesting_agent,
            )

    @staticmethod
    def _active_confirmations(events: list[Event]) -> dict[str, ActiveConfirmation]:
        answered_ids: set[str] = set()
        requests: list[tuple[Event, Any]] = []
        for event in events:
            for response in event.get_function_responses():
                if response.name == REQUEST_CONFIRMATION and response.id:
                    answered_ids.add(response.id)
            for call in event.get_function_calls():
                if call.name == REQUEST_CONFIRMATION and call.id:
                    requests.append((event, call))

        result: dict[str, ActiveConfirmation] = {}
        for event, call in requests:
            if call.id in answered_ids or not call.args:
                continue
            original = call.args.get("originalFunctionCall") or {}
            args = original.get("args") or {}
            action = str(original.get("name") or "acao")
            details = {
                key: str(value)
                for key, value in args.items()
                if key in {"area", "data", "nome"}
            }
            result[call.id] = ActiveConfirmation(
                confirmation_id=call.id,
                invocation_id=event.invocation_id,
                requesting_agent=event.author,
                action=action,
                details=details,
                payload={"original_function_call": original},
            )
        return result

    @staticmethod
    def _final_response(events: list[Event]) -> str:
        texts: list[str] = []
        for event in events:
            if event.author == "user" or not event.content:
                continue
            for part in event.content.parts or []:
                if part.text:
                    texts.append(part.text)
        return "\n".join(texts).strip()

    def _runner(self) -> Runner:
        if self.runner is None:
            raise RuntimeError("Runner não iniciado.")
        return self.runner

    def _session_service(self) -> SqliteSessionService:
        if self.session_service is None:
            raise RuntimeError("Serviço de sessão não iniciado.")
        return self.session_service


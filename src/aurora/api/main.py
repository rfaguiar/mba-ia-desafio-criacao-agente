from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from aurora.api.schemas import (
    ConfirmationRequest,
    ConversationResponse,
    CreateSessionRequest,
    CreateSessionResponse,
    MessageRequest,
)
from aurora.config import settings
from aurora.domain.exceptions import (
    ConfirmationInvalidError,
    DomainError,
    SessionNotFoundError,
)
from aurora.domain.reservations import ReservationService
from aurora.domain.visitors import VisitorService
from aurora.runtime.conversation import ConversationService


def create_app(runtime: ConversationService | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        if runtime is None:
            configured_runtime = ConversationService(
                database_url=settings.database_url,
                seed_directory=settings.seed_directory,
                model=settings.gemini_model,
                api_key=settings.require_google_api_key(),
            )
        else:
            configured_runtime = runtime
        await configured_runtime.start()
        app.state.runtime = configured_runtime
        try:
            yield
        finally:
            await configured_runtime.close()

    app = FastAPI(
        title="Residencial Aurora",
        description="API do assistente virtual do Residencial Aurora.",
        version="0.1.0",
        lifespan=lifespan,
    )

    @app.exception_handler(SessionNotFoundError)
    async def session_not_found_handler(
        request: Request,
        error: SessionNotFoundError,
    ) -> JSONResponse:
        del request
        return JSONResponse(
            status_code=404,
            content={"codigo": error.code, "mensagem": error.message},
        )

    @app.exception_handler(ConfirmationInvalidError)
    async def confirmation_invalid_handler(
        request: Request,
        error: ConfirmationInvalidError,
    ) -> JSONResponse:
        del request
        return JSONResponse(
            status_code=409,
            content={"codigo": error.code, "mensagem": error.message},
        )

    @app.exception_handler(DomainError)
    async def domain_error_handler(
        request: Request,
        error: DomainError,
    ) -> JSONResponse:
        del request
        return JSONResponse(
            status_code=409,
            content={"codigo": error.code, "mensagem": error.message},
        )

    @app.post("/sessoes", status_code=201, response_model=CreateSessionResponse)
    async def create_session(
        payload: CreateSessionRequest,
        request: Request,
    ) -> CreateSessionResponse:
        try:
            session_id = await request.app.state.runtime.create_session(
                payload.apartamento
            )
        except ValueError as error:
            return JSONResponse(
                status_code=422,
                content={"codigo": "apartamento_invalido", "mensagem": str(error)},
            )
        return CreateSessionResponse(session_id=session_id)

    @app.post(
        "/sessoes/{session_id}/mensagens",
        response_model=ConversationResponse,
    )
    async def send_message(
        session_id: str,
        payload: MessageRequest,
        request: Request,
    ) -> ConversationResponse:
        result = await request.app.state.runtime.send_message(
            session_id,
            payload.texto,
        )
        return ConversationResponse.model_validate(result)

    @app.post(
        "/sessoes/{session_id}/confirmacoes",
        response_model=ConversationResponse,
    )
    async def respond_confirmation(
        session_id: str,
        payload: ConfirmationRequest,
        request: Request,
    ) -> ConversationResponse:
        result = await request.app.state.runtime.respond_confirmation(
            session_id,
            payload.id,
            payload.confirmado,
        )
        return ConversationResponse.model_validate(result)

    @app.get("/sessoes/{session_id}/eventos")
    async def get_events(session_id: str, request: Request) -> list[dict]:
        return await request.app.state.runtime.get_events(session_id)

    @app.get("/apartamentos/{apartamento}/reservas")
    async def list_reservations(
        apartamento: str,
        request: Request,
    ) -> list[dict[str, str]]:
        service = ReservationService(request.app.state.runtime.database)
        return await service.list_apartment(apartamento)

    @app.get("/apartamentos/{apartamento}/visitantes")
    async def list_visitors(
        apartamento: str,
        request: Request,
    ) -> list[dict[str, str]]:
        service = VisitorService(request.app.state.runtime.database)
        return await service.list_apartment(apartamento)

    return app


app = create_app()


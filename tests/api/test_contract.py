from fastapi.testclient import TestClient

from aurora.api.main import create_app
from aurora.domain.exceptions import ConfirmationInvalidError, SessionNotFoundError


class FakeRuntime:
    def __init__(self) -> None:
        self.database = object()
        self.confirmation_calls: list[tuple[str, str, bool]] = []

    async def start(self) -> None:
        return None

    async def close(self) -> None:
        return None

    async def create_session(self, apartment: str) -> str:
        return f"session-{apartment}"

    async def send_message(self, session_id: str, text: str) -> dict:
        if session_id == "missing":
            raise SessionNotFoundError
        return {
            "resposta": text,
            "confirmacoes_pendentes": [
                {
                    "id": "confirmation-1",
                    "acao": "reserve_common_area",
                    "detalhes": {"area": "salao-de-festas", "data": "2030-04-20"},
                }
            ],
        }

    async def respond_confirmation(
        self,
        session_id: str,
        confirmation_id: str,
        confirmed: bool,
    ) -> dict:
        if confirmation_id == "invalid":
            raise ConfirmationInvalidError
        self.confirmation_calls.append((session_id, confirmation_id, confirmed))
        return {"resposta": "ok", "confirmacoes_pendentes": []}

    async def get_events(self, session_id: str) -> list[dict]:
        if session_id == "missing":
            raise SessionNotFoundError
        return [{"author": "user", "content": {"text": "hello"}}]


def test_session_message_and_confirmation_contract() -> None:
    runtime = FakeRuntime()
    with TestClient(create_app(runtime)) as client:
        created = client.post("/sessoes", json={"apartamento": "101"})
        message = client.post(
            "/sessoes/session-101/mensagens",
            json={"texto": "reserve"},
        )
        confirmation = client.post(
            "/sessoes/session-101/confirmacoes",
            json={"id": "confirmation-1", "confirmado": True},
        )

    assert created.status_code == 201
    assert created.json() == {"session_id": "session-101"}
    assert message.status_code == 200
    assert set(message.json()) == {"resposta", "confirmacoes_pendentes"}
    assert confirmation.json() == {"resposta": "ok", "confirmacoes_pendentes": []}
    assert runtime.confirmation_calls == [
        ("session-101", "confirmation-1", True)
    ]


def test_invalid_confirmation_is_409_and_missing_session_is_404() -> None:
    with TestClient(create_app(FakeRuntime())) as client:
        invalid = client.post(
            "/sessoes/session-101/confirmacoes",
            json={"id": "invalid", "confirmado": True},
        )
        missing_message = client.post(
            "/sessoes/missing/mensagens",
            json={"texto": "hello"},
        )
        missing_events = client.get("/sessoes/missing/eventos")

    assert invalid.status_code == 409
    assert missing_message.status_code == 404
    assert missing_events.status_code == 404


def test_request_models_reject_unknown_fields() -> None:
    with TestClient(create_app(FakeRuntime())) as client:
        response = client.post(
            "/sessoes",
            json={"apartamento": "101", "morador": "inventado"},
        )

    assert response.status_code == 422

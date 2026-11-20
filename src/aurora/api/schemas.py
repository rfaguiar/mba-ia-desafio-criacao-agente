from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CreateSessionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    apartamento: str = Field(min_length=1)


class CreateSessionResponse(BaseModel):
    session_id: str


class MessageRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    texto: str = Field(min_length=1)


class ConfirmationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    confirmado: bool


class PendingConfirmationResponse(BaseModel):
    id: str
    acao: str
    detalhes: dict[str, Any]


class ConversationResponse(BaseModel):
    resposta: str
    confirmacoes_pendentes: list[PendingConfirmationResponse]


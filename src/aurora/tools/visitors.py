from google.adk.tools import FunctionTool, ToolContext

from aurora.domain.exceptions import DomainError
from aurora.domain.identity import resolve_identity
from aurora.domain.visitors import VisitorService
from aurora.persistence.database import Database


def visitor_tools(
    database: Database,
    service: VisitorService,
) -> list[FunctionTool]:
    async def list_my_visitors(tool_context: ToolContext) -> dict:
        """Lista visitantes autorizados somente para o apartamento da sessão."""
        identity = await resolve_identity(database, tool_context.session.id)
        return {"visitantes": await service.list_own(identity)}

    async def authorize_visitor(
        nome: str,
        data: str,
        tool_context: ToolContext,
    ) -> dict:
        """Autoriza um visitante; o sistema exige confirmação antes da execução."""
        identity = await resolve_identity(database, tool_context.session.id)
        try:
            return await service.authorize(identity, nome, data)
        except DomainError as error:
            return {"error": error.message, "codigo": error.code}

    return [
        FunctionTool(list_my_visitors),
        FunctionTool(authorize_visitor, require_confirmation=True),
    ]


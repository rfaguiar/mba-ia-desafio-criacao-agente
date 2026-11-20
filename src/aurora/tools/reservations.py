from google.adk.tools import FunctionTool, ToolContext

from aurora.domain.exceptions import DomainError
from aurora.domain.identity import resolve_identity
from aurora.domain.reservations import ReservationService
from aurora.persistence.database import Database


def reservation_tools(
    database: Database,
    service: ReservationService,
) -> list[FunctionTool]:
    async def list_my_reservations(tool_context: ToolContext) -> dict:
        """Lista apenas as reservas ativas do apartamento autenticado na sessão."""
        identity = await resolve_identity(database, tool_context.session.id)
        return {"reservas": await service.list_own(identity)}

    async def check_area_availability(area: str, data: str) -> dict:
        """Consulta se uma área está livre, sem revelar quem possui a reserva."""
        try:
            return await service.availability(area, data)
        except DomainError as error:
            return {"error": error.message, "codigo": error.code}

    async def cancel_my_reservation(
        area: str,
        data: str,
        tool_context: ToolContext,
    ) -> dict:
        """Cancela, sem confirmação, somente uma reserva do apartamento da sessão."""
        identity = await resolve_identity(database, tool_context.session.id)
        try:
            return await service.cancel_own(identity, area, data)
        except DomainError as error:
            return {"error": error.message, "codigo": error.code}

    async def reserve_common_area(
        area: str,
        data: str,
        tool_context: ToolContext,
    ) -> dict:
        """Reserva uma área para a data; a confirmação é exigida pelo sistema."""
        identity = await resolve_identity(database, tool_context.session.id)
        try:
            return await service.create(identity, area, data)
        except DomainError as error:
            return {"error": error.message, "codigo": error.code}

    async def requires_reservation_confirmation(
        area: str,
        data: str,
        tool_context: ToolContext,
    ) -> bool:
        del tool_context
        try:
            return await service.requires_confirmation(area, data)
        except DomainError:
            return True

    return [
        FunctionTool(list_my_reservations),
        FunctionTool(check_area_availability),
        FunctionTool(cancel_my_reservation),
        FunctionTool(
            reserve_common_area,
            require_confirmation=requires_reservation_confirmation,
        ),
    ]


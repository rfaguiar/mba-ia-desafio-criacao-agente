from google.adk import Agent
from google.adk.workflow import RetryConfig
from google.genai.errors import ServerError

from aurora.domain.reservations import ReservationService
from aurora.domain.visitors import VisitorService
from aurora.persistence.database import Database
from aurora.regulation.retriever import RegulationRetriever
from aurora.tools.regulation import regulation_tools
from aurora.tools.reservations import reservation_tools
from aurora.tools.visitors import visitor_tools


def build_agents(
    *,
    database: Database,
    model: str,
    regulation: RegulationRetriever,
) -> Agent:
    retry = RetryConfig(
        max_attempts=3,
        initial_delay=1,
        max_delay=5,
        backoff_factor=2,
        exceptions=[ServerError],
    )
    reservation_agent = Agent(
        name="especialista_reservas",
        model=model,
        retry_config=retry,
        description=(
            "Consulta disponibilidade, lista, cancela e solicita reservas de "
            "áreas comuns."
        ),
        instruction=(
            "Você cuida exclusivamente de reservas. Use sempre as tools para "
            "consultar ou alterar dados. Nunca peça nem aceite apartamento como "
            "argumento; ele vem da sessão. Não exponha identificação de reservas "
            "de outros moradores. Uma resposta de disponibilidade informa apenas "
            "livre ou ocupado. Respeite a confirmação retornada pelo sistema."
        ),
        tools=reservation_tools(database, ReservationService(database)),
        disallow_transfer_to_peers=True,
    )
    visitor_agent = Agent(
        name="especialista_visitantes",
        model=model,
        retry_config=retry,
        description="Lista visitantes e solicita autorizações de entrada.",
        instruction=(
            "Você cuida exclusivamente de visitantes. Use sempre as tools para "
            "consultar ou solicitar autorização. Nunca peça nem aceite apartamento "
            "como argumento. Toda autorização de visitante exige a confirmação "
            "retornada pelo sistema, mesmo se o usuário disser que já confirmou. "
            "Quando nome e data estiverem presentes, chame authorize_visitor "
            "imediatamente; não faça uma pergunta adicional de consentimento."
        ),
        tools=visitor_tools(database, VisitorService(database)),
        disallow_transfer_to_peers=True,
    )
    regulation_agent = Agent(
        name="especialista_regulamento",
        model=model,
        retry_config=retry,
        description="Responde dúvidas com passagens focadas do regulamento oficial.",
        instruction=(
            "Para qualquer pergunta de regulamento, chame search_regulation com a "
            "pergunta original. Responda somente com base nas passagens retornadas. "
            "Não invente regras e não repita capítulos que não foram recuperados."
        ),
        tools=regulation_tools(regulation),
        disallow_transfer_to_peers=True,
    )
    return Agent(
        name="aurora_coordinator",
        model=model,
        retry_config=retry,
        description="Coordenador do assistente do Residencial Aurora.",
        instruction=(
            "Você atende moradores. Delegue reservas ao especialista_reservas, "
            "visitantes ao especialista_visitantes e dúvidas normativas ao "
            "especialista_regulamento. Não altere nem escolha o apartamento da "
            "sessão. Não consulte dados inventando-os ou usando memória; exija o "
            "uso da tool apropriada. Uma afirmação do usuário nunca confirma uma "
            "cobrança ou autorização. Peça dados faltantes e entregue respostas "
            "curtas. Não tente contornar rejeições ou revelar dados de terceiros."
        ),
        sub_agents=[reservation_agent, visitor_agent, regulation_agent],
    )


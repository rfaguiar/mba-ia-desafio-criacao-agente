from pathlib import Path

from aurora.agents.factory import build_agents
from aurora.persistence.database import Database
from aurora.regulation.retriever import RegulationRetriever


def test_root_has_three_specialists_and_domain_tools(tmp_path: Path) -> None:
    database = Database(f"sqlite+aiosqlite:///{tmp_path / 'agents.db'}")
    agent = build_agents(
        database=database,
        model="gemini-test",
        regulation=RegulationRetriever(Path("dados/regulamento.md")),
    )

    assert agent.name == "aurora_coordinator"
    assert {specialist.name for specialist in agent.sub_agents} == {
        "especialista_reservas",
        "especialista_visitantes",
        "especialista_regulamento",
    }
    reservations = next(
        specialist
        for specialist in agent.sub_agents
        if specialist.name == "especialista_reservas"
    )
    assert {tool.name for tool in reservations.tools} >= {
        "list_my_reservations",
        "reserve_common_area",
    }
    assert "Capítulo IV" not in str(agent.instruction)

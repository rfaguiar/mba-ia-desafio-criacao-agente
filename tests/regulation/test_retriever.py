from pathlib import Path

from aurora.regulation.retriever import RegulationRetriever


def test_retrieval_returns_pool_sunday_hours_only_from_relevant_article() -> None:
    retriever = RegulationRetriever(Path("dados/regulamento.md"))

    passages = retriever.search("Até que horas a piscina funciona aos domingos?")

    assert passages
    assert "Art. 22" in passages[0].article
    assert "9h às 20h" in passages[0].text
    assert "Art. 16" not in "\n".join(passage.text for passage in passages)

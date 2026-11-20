from google.adk.tools import FunctionTool

from aurora.regulation.retriever import RegulationRetriever


def regulation_tools(retriever: RegulationRetriever) -> list[FunctionTool]:
    def search_regulation(question: str) -> dict:
        """Busca somente artigos pertinentes do regulamento interno oficial."""
        passages = retriever.search(question)
        return {
            "passagens": [
                {
                    "capitulo": passage.chapter,
                    "artigo": passage.article,
                    "texto": passage.text,
                }
                for passage in passages
            ]
        }

    return [FunctionTool(search_regulation)]


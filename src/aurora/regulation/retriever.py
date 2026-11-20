import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class RegulationPassage:
    chapter: str
    article: str
    text: str


def _normalize(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value)
    return "".join(
        char for char in ascii_value if not unicodedata.combining(char)
    ).lower()


class RegulationRetriever:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.passages = self._parse(path.read_text(encoding="utf-8"))

    def search(self, query: str, limit: int = 2) -> list[RegulationPassage]:
        query_terms = {
            word
            for word in re.findall(r"[a-z0-9]+", _normalize(query))
            if len(word) >= 3
        }
        ranked: list[tuple[int, int, RegulationPassage]] = []
        for index, passage in enumerate(self.passages):
            haystack = _normalize(f"{passage.chapter} {passage.text}")
            score = sum(term in haystack for term in query_terms)
            if score:
                ranked.append((score, -index, passage))
        ranked.sort(key=lambda item: (item[0], item[1]), reverse=True)
        return [item[2] for item in ranked[:limit]]

    @staticmethod
    def _parse(source: str) -> list[RegulationPassage]:
        chapter = ""
        article = ""
        article_lines: list[str] = []
        passages: list[RegulationPassage] = []

        def flush() -> None:
            if article and article_lines:
                text = "\n".join(article_lines).strip()
                passages.append(RegulationPassage(chapter, article, text))
                article_lines.clear()

        for line in source.splitlines():
            if line.startswith("## "):
                flush()
                chapter = line.removeprefix("## ").strip()
                article = ""
            elif re.match(r"^\*\*Art\.\s*\d+", line):
                flush()
                article = line.split("**", 2)[1]
                article_lines.append(line)
            elif article and line.strip():
                article_lines.append(line)
        flush()
        return passages


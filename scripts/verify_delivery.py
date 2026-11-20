import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(f"FALHA: {message}")


def main() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    if not re.search(r'"google-adk==2\.9\.1"', pyproject):
        fail("ADK 2.9.1 não está fixado exatamente no pyproject.toml.")

    lock = (ROOT / "uv.lock").read_text(encoding="utf-8")
    if 'name = "google-adk"' not in lock or 'version = "2.9.1"' not in lock:
        fail("uv.lock não fixa google-adk 2.9.1.")

    env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
    required_names = {
        "GOOGLE_API_KEY",
        "GEMINI_MODEL",
        "DATABASE_URL",
        "SEED_DIRECTORY",
        "HOST",
        "PORT",
    }
    listed_names = {line.strip() for line in env_example.splitlines() if line.strip()}
    if listed_names != required_names:
        fail(".env.example deve conter somente os nomes das variáveis documentadas.")
    if any("=" in line for line in env_example.splitlines()):
        fail(".env.example não pode conter valores.")

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    if ".env" not in gitignore.splitlines():
        fail(".env não está ignorado.")

    result = subprocess.run(
        ["git", "diff", "--exit-code", "--", "dados"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        fail("os arquivos em dados/ foram alterados.")

    agent = (ROOT / "src/aurora/agents/factory.py").read_text(encoding="utf-8")
    for specialist in (
        "especialista_reservas",
        "especialista_visitantes",
        "especialista_regulamento",
    ):
        if specialist not in agent:
            fail(f"especialista ausente: {specialist}")

    forbidden_patterns = [
        re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
        re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    ]
    candidates = [
        *ROOT.glob("src/**/*.py"),
        *ROOT.glob("scripts/**/*.py"),
        *ROOT.glob("tests/**/*.py"),
        ROOT / "pyproject.toml",
    ]
    for path in candidates:
        content = path.read_text(encoding="utf-8")
        if any(pattern.search(content) for pattern in forbidden_patterns):
            fail(f"possível credencial encontrada em {path.relative_to(ROOT)}")

    print("Entrega verificada: dados integros, ADK fixado e sem credenciais.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"FALHA: {error}", file=sys.stderr)
        raise SystemExit(1) from error

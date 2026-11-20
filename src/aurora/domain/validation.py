from datetime import date

from aurora.domain.exceptions import ValidationError


def validate_date(value: str) -> str:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise ValidationError("A data deve usar o formato AAAA-MM-DD.") from error
    if parsed.isoformat() != value:
        raise ValidationError("A data deve usar o formato AAAA-MM-DD.")
    return value


def validate_visitor_name(value: str) -> str:
    normalized = " ".join(value.split())
    if not normalized or len(normalized) > 200:
        raise ValidationError("Informe o nome do visitante com até 200 caracteres.")
    return normalized


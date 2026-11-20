class DomainError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class SessionNotFoundError(DomainError):
    def __init__(self) -> None:
        super().__init__("sessao_inexistente", "Sessão não encontrada.")


class ReservationConflictError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            "data_indisponivel",
            "A área já está reservada para esta data.",
        )


class ConfirmationInvalidError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            "confirmacao_invalida",
            "Confirmação inexistente ou já respondida nesta sessão.",
        )


class ValidationError(DomainError):
    def __init__(self, message: str) -> None:
        super().__init__("dados_invalidos", message)


from typing import Any


class Disponibilidade:
    def __init__(self, nome, segunda, terca, quarta, quinta, sexta):
        self.nome = nome
        self.segunda = segunda
        self.terca = terca
        self.quarta = quarta
        self.quinta = quinta
        self.sexta = sexta

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def __str__(self) -> str:
        return super().__str__()

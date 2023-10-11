from typing import Any, Type


class Cromossome:

    def __init__(self):
        self.cromossome = []
        self.nota = 0

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def __str__(self) -> str:
        return super().__str__()

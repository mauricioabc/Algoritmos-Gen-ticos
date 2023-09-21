from typing import Any, Type
from Entities.Disciplina import Disciplina


class Curso:
    def __init__(self, nome, turno, dia_inicio, dia_fim):
        self.nome = nome
        self.turno = turno
        self.dia_inicio = dia_inicio
        self.dia_fim = dia_fim
        self.lista_disciplinas = []

    def adicionar_disciplina(self, nome=None, fase=None, carga_horaria=None, professor=None, disciplina=None):
        if disciplina is not None:
            self.lista_disciplinas.append(disciplina)
        else:
            nova_disciplina = Disciplina(nome, fase, carga_horaria, professor)
            self.lista_disciplinas.append(nova_disciplina)

    def getNumeroDias(self):
        if self.dia_inicio=='Segunda':
            return 5
        elif self.dia_inicio=='Terça':
            return 4

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def __str__(self) -> str:
        return super().__str__()

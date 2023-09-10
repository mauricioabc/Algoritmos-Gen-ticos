import unittest
from Entities.Curso import Curso
from Entities.Disciplina import Disciplina
from Entities.Disponibilidade import Disponibilidade


class TestCurso(unittest.TestCase):

    def setUp(self):
        self.curso = Curso('Nome', 'Turno', 'Segunda', 'Terça')

    def test_nome(self):
        self.assertEqual(self.curso.nome, 'Nome')

    def test_turno(self):
        self.assertEqual(self.curso.turno, 'Turno')

    def test_dias_semana(self):
        self.assertEqual(self.curso.dia_inicio, 'Segunda')
        self.assertEqual(self.curso.dia_fim, 'Terça')

    def test_set_attr(self):
        self.curso.turno = "Matutino"
        self.assertEqual(self.curso.turno, 'Matutino')

    def test_get_attr(self):
        teste = self.curso.turno
        self.assertEqual(teste, 'Turno')

    def test_disciplina(self):
        disciplina = Disciplina('Nome', 2, 80, 'Professor')
        self.curso.adicionar_disciplina(disciplina=disciplina)
        disciplina = Disciplina('Nome', 3, 80, 'Professor')
        self.curso.adicionar_disciplina(disciplina=disciplina)
        teste = self.curso.lista_disciplinas[0]
        self.assertEqual(teste.nome, 'Nome')

    def test_disponibilidade(self):
        disponibilidade = Disponibilidade('Teste', 'S', 'S', 'S', 'N', 'N')
        self.assertEqual(disponibilidade.quinta, 'N')

if __name__ == '__main__':
    unittest.main()

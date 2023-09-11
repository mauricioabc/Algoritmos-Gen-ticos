import unittest
from Infraestructure.Parser import Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
        self.lista_cursos = None
        self.lista_disponibilidade = None

    def test_process_curso(self):
        self.lista_cursos = self.parser.process_cursos()
        self.assertEqual(self.lista_cursos[0].nome, 'Ciência da Computação (Matutino)')

    def test_process_disponibilidade(self):
        self.lista_cursos = self.parser.process_disponibilidade()
        self.assertEqual(self.lista_cursos[0].nome, 'Ailton Durigon')

    def test_process_configs(self):
        self.lista_cursos, self.lista_disponibilidade = self.parser.process_configs()
        self.assertEqual(self.lista_cursos[0].nome, 'Ciência da Computação (Matutino)')
        self.assertEqual(self.lista_disponibilidade[0].nome, 'Ailton Durigon')


if __name__ == '__main__':
    unittest.main()

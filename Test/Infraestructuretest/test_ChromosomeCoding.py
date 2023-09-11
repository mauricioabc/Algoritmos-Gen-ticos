import unittest
from Infraestructure.Parser import Parser
from Infraestructure.ChromosomeCoding import ChromosomeCoding


class TestChromosomeCoding(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
        self.chromesome = ChromosomeCoding(10)
        self.lista_cursos = None
        self.lista_disponibilidade = None

    def test_process_chromosome_generator(self):
        self.lista_cursos, self.lista_disponibilidade = self.parser.process_configs()
        cromossomos = self.chromesome.process_initial_chromosomes(self.lista_cursos)

    def test_preenchimento_dos_cromossomos_2_fase_CC(self):
        self.lista_cursos, self.lista_disponibilidade = self.parser.process_configs()
        cromossomos = self.chromesome.process_initial_chromosomes(self.lista_cursos)
        cromossomos_CC = cromossomos[0]
        cromossomo = cromossomos_CC[0]
        cromossomo_2_fase_CC = cromossomo[:10]
        teste = True
        for pos in range(10):
            if cromossomo_2_fase_CC[pos] > 5:
                teste = False
        self.assertEqual(teste, True)


if __name__ == '__main__':
    unittest.main()

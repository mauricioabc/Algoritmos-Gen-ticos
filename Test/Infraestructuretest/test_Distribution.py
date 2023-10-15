import unittest
from Distribution.DistributionConnector import DistributionConnector
from Infraestructure.Parser import Parser
from Infraestructure.ChromosomeCoding import ChromosomeCoding


class TestDistribution(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
        self.chromesome = ChromosomeCoding(10)
        self.lista_cursos = None
        self.lista_disponibilidade = None
        self.lista_todas_disciplinas = None

    def test_distribuicao(self):
        self.lista_cursos, self.lista_disponibilidade, self.lista_todas_disciplinas = self.parser.process_configs()
        cromossomos = self.chromesome.process_initial_chromosomes(self.lista_cursos)
        connector = DistributionConnector(self.lista_cursos, self.lista_todas_disciplinas, self.lista_disponibilidade)
        resultado = connector.process_av_carga_horaria(cromossomos)
        print('Teste')




if __name__ == '__main__':
    unittest.main()

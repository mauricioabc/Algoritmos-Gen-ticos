from Infraestructure.Logger import Logger
import random


class RandomNumber:

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        random.seed(40028922)

    def random_number_generator(self, intervalo_inicio, intervalo_fim):
        numero_aleatorio = random.randint(intervalo_inicio, intervalo_fim)
        return numero_aleatorio

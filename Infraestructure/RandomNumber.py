from Infraestructure.Logger import Logger
import random


class RandomNumber:

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        random.seed(40028922)

    def int_generator(self, intervalo_inicio, intervalo_fim):
        numero_aleatorio = random.randint(intervalo_inicio, intervalo_fim)
        return numero_aleatorio

    def uniform_generator(self, intervalo_inicio, intervalo_fim):
        numero_aleatorio = random.uniform(intervalo_inicio, intervalo_fim)
        return numero_aleatorio

    def random_shuffle(self, chromosomes_for_crossover):
        return random.shuffle(chromosomes_for_crossover)

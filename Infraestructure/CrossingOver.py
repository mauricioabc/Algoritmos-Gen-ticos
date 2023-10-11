from Infraestructure.Logger import Logger
from Entities.Cromossome import Cromossome
import random


class CrossingOver:

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    def calculates_accumulated_frequency(self, chromossome_list, course_list):
        self.logger.info('Iniciando o cálculo da frequência acumulada dos cromossomos.')
        for i in range(len(chromossome_list)):
            chromossomes = chromossome_list[i]
            self.logger.info('Ordenando e calculando os cromossomos do curso: ' + course_list[i].nome)

            # Ordenar os cromossomos pelo atributo nota em ordem decrescente
            ordered_chromosomes = sorted(chromossomes, key=lambda x: x.nota, reverse=True)

            # Calcular a frequência acumulada
            cumulative_frequency = 0
            for chromossome in ordered_chromosomes:
                cumulative_frequency += chromossome.nota
                chromossome.frequencia_acumulada = cumulative_frequency
            chromossome_list[i] = ordered_chromosomes
            self.logger.info('Finalizando o cálculo dos cromossomos do curso: ' + course_list[i].nome)
        self.logger.info('Finalizando o cálculo da frequência acumulada dos cromossomos.')
        return chromossome_list

    def crossing(self, chromossome_list, course_list, crossing_limit, elitism_limit):
        self.logger.info('Iniciando o cruzamento dos cromossomos.')
        new_generation = []
        for i in range(len(chromossome_list)):
            chromossomes = chromossome_list[i]
            self.logger.info('Cruzando os cromossomos do curso: ' + course_list[i].nome)

            # Selecionar cromossomos para cruzamento com base na frequência acumulada
            chromosomes_for_crossover = [cromossomo for cromossomo in chromossomes[:crossing_limit]]

            # Embaralhar a lista para garantir variedade na escolha
            random.shuffle(chromosomes_for_crossover)

            # Aplicar elitismo para selecionar os melhores cromossomos
            best_chromosomes = sorted(chromossomes, key=lambda x: x.nota)[:elitism_limit]

            # Cruzamento
            nova_geracao = self.realiza_cruzamento(chromosomes_for_crossover)
            nova_geracao.extend(best_chromosomes)

            # Adicionar a nova geração à lista
            new_generation.append(nova_geracao)

        return new_generation

    def realiza_cruzamento(self, cromossomos_para_cruzamento):
        nova_geracao = []
        for i in range(0, len(cromossomos_para_cruzamento), 2):
            pai1 = cromossomos_para_cruzamento[i]
            pai2 = cromossomos_para_cruzamento[i + 1]

            # Lógica de cruzamento
            filho1, filho2 = self.crossover(pai1, pai2)

            # Adicionar os filhos à nova geração
            nova_geracao.append(filho1)
            nova_geracao.append(filho2)

        return nova_geracao

    def crossover(self, pai1, pai2):
        # Lógica do ponto de corte
        ponto_de_corte = random.randint(1, len(pai1.cromossome) - 1)

        # Criar filhos combinando partes dos pais
        filho1 = Cromossome()
        filho1.cromossome = pai1.cromossome[:ponto_de_corte] + pai2.cromossome[ponto_de_corte:]
        filho2 = Cromossome()
        filho2.cromossome = pai2.cromossome[:ponto_de_corte] + pai1.cromossome[ponto_de_corte:]

        return filho1, filho2

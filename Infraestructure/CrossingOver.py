from Infraestructure.Logger import Logger
from Entities.Chromosome import Cromossome
from Infraestructure.RandomNumber import RandomNumber


class CrossingOver:

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.random = RandomNumber()

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

    def crossing(self, chromossome_list, course_list, crossing_limit, elitism_limit, mutation_rate):
        new_generation = []

        # Calcula a frequência acumulada antes do loop de curso
        chromossome_list = self.calculates_accumulated_frequency(chromossome_list, course_list)

        self.logger.info('Iniciando o cruzamento dos cromossomos.')
        for i in range(len(chromossome_list)):
            chromossomes = chromossome_list[i]
            self.logger.info('Cruzando os cromossomos do curso: ' + course_list[i].nome)

            # Selecionar cromossomos para cruzamento com base na frequência acumulada
            chromosomes_for_crossover = self.select_chromosomes_based_on_frequency(chromossomes, crossing_limit)

            # Embaralhar a lista para garantir variedade na escolha
            self.random.random_shuffle(chromosomes_for_crossover)

            # Aplicar elitismo para selecionar os melhores cromossomos
            best_chromosomes = sorted(chromossomes, key=lambda x: x.nota)[:elitism_limit]

            # Cruzamento
            nova_geracao = self.realiza_cruzamento(chromosomes_for_crossover)

            # Aplicar mutação
            nova_geracao = self.aplica_mutacao(nova_geracao, mutation_rate)

            # Adiciona os cromossomos selecionados pelo elitismo
            nova_geracao.extend(best_chromosomes)

            # Adicionar a nova geração à lista
            new_generation.append(nova_geracao)

        self.logger.info('Finalizando o cruzamento dos cromossomos.')
        return new_generation

    def select_chromosomes_based_on_frequency(self, chromossomes, crossing_limit):
        total_frequency = chromossomes[-1].frequencia_acumulada  # Último cromossomo tem a frequência acumulada total
        selected_chromosomes = []

        for _ in range(crossing_limit):
            random_frequency = self.random.uniform_generator(0, total_frequency)
            selected_chromosomes.append(
                next(ch for ch in chromossomes if ch.frequencia_acumulada >= random_frequency)
            )

        return selected_chromosomes

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
        ponto_de_corte = self.random.int_generator(1, len(pai1.cromossome) - 1)

        # Criar filhos combinando partes dos pais
        filho1 = Cromossome()
        filho1.cromossome = pai1.cromossome[:ponto_de_corte] + pai2.cromossome[ponto_de_corte:]
        filho2 = Cromossome()
        filho2.cromossome = pai2.cromossome[:ponto_de_corte] + pai1.cromossome[ponto_de_corte:]

        return filho1, filho2

    def aplica_mutacao(self, cromossomes, mutation_rate):
        for cromossome in cromossomes:
            if self.random.uniform_generator(0, 1) < mutation_rate:
                self.realiza_mutacao(cromossome)
        return cromossomes

    def realiza_mutacao(self, cromossome):
        self.logger.info('Ocorreu uma mutação.')
        # Lógica específica de mutação, modifica aleatoriamente alguns genes do cromossomo
        gene_index = self.random.int_generator(0, len(cromossome.cromossome) - 1)
        novo_valor = self.random.int_generator(0, 1)  # Modifique isso com base na natureza dos seus genes
        cromossome.cromossome[gene_index] = novo_valor

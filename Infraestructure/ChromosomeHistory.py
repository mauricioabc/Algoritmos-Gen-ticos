from Infraestructure.Logger import Logger
from Entities.Chromosome import Cromossome


class ChromosomeHistory:

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)
        self.selected_chromosomes = []
        self.number_generation = 0

    def save_best_chromosomes(self, chromossome_list, course_list, note):
        self.logger.info('Salvando cromossomos de melhor nota.')
        if not self.selected_chromosomes:
            for i in range(len(chromossome_list)):
                chromossomes = chromossome_list[i]
                self.logger.info('Buscando melhor cromossomo do curso: ' + course_list[i].nome)
                best_chromosome = sorted(chromossomes, key=lambda x: x.nota)[:1]
                self.selected_chromosomes.extend(best_chromosome)
                self.logger.info('Cromossomo salvo com sucesso.')
            return self.analyze_stop_classification(note)

        for i in range(len(chromossome_list)):
            chromossomes = chromossome_list[i]
            self.logger.info('Buscando melhor cromossomo do curso: ' + course_list[i].nome)
            best_chromosome = sorted(chromossomes, key=lambda x: x.nota)[:1]
            if self.selected_chromosomes[i].nota < best_chromosome[0].nota:
                self.selected_chromosomes[i] = best_chromosome[0]
            self.logger.info('Cromossomo salvo com sucesso.')
        return self.analyze_stop_classification(note)

    def analyze_stop_classification(self, note):
        self.logger.info('Verificando critério de parada.')
        self.number_generation += 1
        self.logger.info('Número da geração atual: ' + str(self.number_generation))

        # Imprimir conjunto de notas para fins de depuração
        notas_cromossomos = [chromo.nota for chromo in self.selected_chromosomes]
        self.logger.info('Conjunto de notas dos cromossomos: ' + str(notas_cromossomos))

        # Verificar se todos os cromossomos têm nota menor que X
        if all(chromo.nota < note for chromo in self.selected_chromosomes):
            self.logger.info('Critério atendido: todos os cromossomos têm nota menor que ' + str(note) + '.')
            return True
        self.logger.info('Critério não atendido: pelo menos um cromossomo tem nota maior ou igual a ' + str(note) + '.')
        return False

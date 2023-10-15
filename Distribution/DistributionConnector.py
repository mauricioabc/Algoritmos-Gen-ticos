from Infraestructure.Logger import Logger
from Infraestructure.ChromosomeRating import ChromosomeRating
import multiprocessing


class DistributionConnector:

    def __init__(self, lista_cursos, lista_todas_disciplinas, lista_disponibilidade, lista_todos_os_cromossomos):
        self.logger = Logger(self.__class__.__name__)
        self.lista_cursos = lista_cursos
        self.lista_todas_disciplinas = lista_todas_disciplinas
        self.lista_disponibilidade = lista_disponibilidade
        self.lista_todos_os_cromossomos = lista_todos_os_cromossomos

    def process_solicitations(self, chunks, process_code, process_number):
        chromosome_rating = ChromosomeRating()
        results = []
        try:
            self.logger.info(f'Running process number: {process_number}')
            if process_code == 0:
                converted_chunk = [chunks]
                local_lista_cursos = self.lista_cursos
                resultado = chromosome_rating.av_carga_horaria(converted_chunk, local_lista_cursos)
                results.extend(resultado)
            elif process_code == 1:
                converted_chunk = [chunks]
                local_lista_cursos = self.lista_cursos
                resultado = chromosome_rating.av_choque_horario(converted_chunk, self.lista_todos_os_cromossomos, self.lista_todas_disciplinas, local_lista_cursos)
                results.append(resultado)
            elif process_code == 2:
                converted_chunk = [chunks]
                local_lista_cursos = self.lista_cursos
                resultado = chromosome_rating.av_disponibilidade(converted_chunk, self.lista_disponibilidade, self.lista_todas_disciplinas, local_lista_cursos)
                results.append(resultado)
            return results
        except Exception as e:
            self.logger.error(f"Erro durante o processamento paralelo: {e}")

    def process_av_carga_horaria(self, lista_cromossomos):
        self.logger.info('Iniciando processamento distribuído de avaliação: carga horária dos cursos.')

        results = []
        results_distribution = []
        try:
            # Número máximo de processos simultâneos
            max_processes = len(lista_cromossomos)  # Corresponde à quantidade de cromossomos

            with multiprocessing.Pool(processes=max_processes) as pool:
                results_distribution = pool.starmap(self.process_solicitations, [(chunks, 0, i) for i, chunks in enumerate(lista_cromossomos)])

                # Indica que nenhum outro trabalho será adicionado ao pool
                pool.close()
                # Espera até que todos os processos tenham concluído
                pool.join()

            for result_line in results_distribution:
                result_chromosome = result_line[0]
                results.append(result_chromosome)

        except Exception as e:
            self.logger.error(f"Erro no processamento dos processos: {e}")

        self.logger.info('Finalizando processamento distribuído de avaliação: carga horária dos cursos.')
        return results

    def process_av_choque_horario(self, lista_cromossomos):
        self.logger.info('Iniciando processamento distribuído de avaliação: choques de horário.')

        results = []
        results_distribution = []
        try:
            # Número máximo de processos simultâneos
            max_processes = len(lista_cromossomos)  # Corresponde à quantidade de cromossomos

            with multiprocessing.Pool(processes=max_processes) as pool:
                results_distribution = pool.starmap(self.process_solicitations,
                                                    [(chunks, 1, i) for i, chunks in enumerate(lista_cromossomos)])

                # Indica que nenhum outro trabalho será adicionado ao pool
                pool.close()
                # Espera até que todos os processos tenham concluído
                pool.join()

            for result_line in results_distribution:
                result_chromosome = result_line[0][0]
                results.append(result_chromosome)

        except Exception as e:
            self.logger.error(f"Erro no processamento dos processos: {e}")

        self.logger.info('Finalizando processamento distribuído de avaliação: choques de horário.')
        return results

    def process_av_disponibilidade(self, lista_cromossomos):
        self.logger.info('Iniciando processamento distribuído de avaliação: disponibilidade dos professores.')

        results = []
        results_distribution = []
        try:
            # Número máximo de processos simultâneos
            max_processes = len(lista_cromossomos)  # Corresponde à quantidade de cromossomos

            with multiprocessing.Pool(processes=max_processes) as pool:
                results_distribution = pool.starmap(self.process_solicitations,
                                                    [(chunks, 2, i) for i, chunks in enumerate(lista_cromossomos)])

                # Indica que nenhum outro trabalho será adicionado ao pool
                pool.close()
                # Espera até que todos os processos tenham concluído
                pool.join()

            for result_line in results_distribution:
                result_chromosome = result_line[0][0]
                results.append(result_chromosome)

        except Exception as e:
            self.logger.error(f"Erro no processamento dos processos: {e}")

        self.logger.info('Finalizando processamento distribuído de avaliação: disponibilidade dos professores.')
        return results



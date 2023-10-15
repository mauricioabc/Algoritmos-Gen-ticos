from Infraestructure.Logger import Logger
import multiprocessing
import xmlrpc.client


class DistributionConnector:

    def __init__(self, lista_cursos, lista_todas_disciplinas, lista_disponibilidade):
        self.logger = Logger(self.__class__.__name__)
        self.lista_cursos = lista_cursos
        self.lista_todas_disciplinas = lista_todas_disciplinas
        self.lista_disponibilidade = lista_disponibilidade

    def process_solicitations(self, chunk, process_code):
        results = []
        try:
            self.logger.info('Running RPC client...')
            client = xmlrpc.client.ServerProxy("http://localhost:8000")
            if process_code == 0:
                resultado = client.av_carga_horaria(chunk, self.lista_cursos)
                results.append(resultado)
            elif process_code == 1:
                resultado = client.av_choque_horario(chunk, self.lista_todas_disciplinas, self.lista_cursos)
                results.append(resultado)
            elif process_code == 2:
                resultado = client.av_choque_horario(chunk, self.lista_disponibilidade, self.lista_todas_disciplinas,
                                                     self.lista_cursos)
                results.append(resultado)
            return results
        except Exception as e:
            self.logger.error(f"Erro durante a chamada XML-RPC: {e}")

    def process_av_carga_horaria(self, lista_cromossomos):
        self.logger.info('Iniciando processamento distribuído de avaliação: carga horária dos cursos.')

        results = []

        for curso, cromossomos in zip(self.lista_cursos, lista_cromossomos):
            self.logger.info(f'Processando os cromossomos do curso: {curso.nome}')

            # Número máximo de processos simultâneos
            max_processes = len(cromossomos)  # Corresponde à quantidade de cromossomos

            # Usando Pool para criar processos em paralelo
            with multiprocessing.Pool(processes=max_processes) as pool:
                # Mapeia a função process_solicitations para os grupos de cromossomos
                results.extend(pool.starmap(self.process_solicitations, [(cromossomos, 0)] * len(cromossomos)))

        self.logger.info('Finalizando processamento distribuído de avaliação: carga horária dos cursos.')
        return results



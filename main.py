import time
from datetime import datetime, timedelta
from Infraestructure.Parser import Parser
from Infraestructure.ChromosomeCoding import ChromosomeCoding
from Infraestructure.ChromosomeRating import ChromosomeRating
from Infraestructure.CrossingOver import CrossingOver
from Infraestructure.ChromosomeHistory import ChromosomeHistory
from Distribution.DistributionConnector import DistributionConnector

def main():
    start_time = time.time()
    # Busca e internaliza os dados dos professores e turmas
    parser = Parser()
    lista_cursos, lista_disponibilidade, lista_todas_disciplinas = parser.process_configs()

    # Recebe a lista de cursos e a população inicial
    # Faz a montagem dos cromossomos por curso
    chromesome_creation = ChromosomeCoding(10)
    lista_cromossomos = chromesome_creation.process_initial_chromosomes(lista_cursos)

    # Cria objetos
    chromesome_rating = ChromosomeRating()
    chromosome_history = ChromosomeHistory()
    chromesome_crossing_over = CrossingOver(lista_todas_disciplinas)

    status = False
    is_distributed = True
    while not status:
        # Faz a avaliação dos cromossomos criados de conforme os critérios
        # Critério: Integralizar a carga horária corretamente (-10 para cada aula faltante)
        # Critério: Não ter choque de horário do professor (-5 a cada choque)
        # Critério: Professor indisponível (-3 a cada indisponibilidade)
        if not is_distributed:
            lista_cromossomos = chromesome_rating.av_carga_horaria(lista_cromossomos, lista_cursos)
            lista_cromossomos = chromesome_rating.av_choque_horario(lista_cromossomos, lista_todas_disciplinas, lista_cursos)
            lista_cromossomos = chromesome_rating.av_disponibilidade(lista_cromossomos, lista_disponibilidade, lista_todas_disciplinas, lista_cursos)
        else:
            connector = DistributionConnector(lista_cursos, lista_todas_disciplinas, lista_disponibilidade, lista_cromossomos)
            lista_cromossomos = connector.process_av_carga_horaria(lista_cromossomos)
            lista_cromossomos = connector.process_av_choque_horario(lista_cromossomos)
            lista_cromossomos = connector.process_av_disponibilidade(lista_cromossomos)

        # Salva melhores notas
        status = chromosome_history.save_best_chromosomes(lista_cromossomos, lista_cursos, 100)

        # Faz a frequência e o cruzamento
        lista_cromossomos = chromesome_crossing_over.crossing(lista_cromossomos, lista_cursos, 8, 2, 0.01)

    end_time = time.time()

    # Formata o tempo
    elapsed_time = end_time - start_time
    elapsed_timedelta = timedelta(seconds=elapsed_time)
    hours, remainder = divmod(elapsed_timedelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(elapsed_timedelta.microseconds / 1000)
    formatted_time = "{:02}:{:02}:{:02}.{:03}".format(hours, minutes, seconds, milliseconds)
    print('Tempo de execução:', formatted_time)


if __name__ == '__main__':
    main()

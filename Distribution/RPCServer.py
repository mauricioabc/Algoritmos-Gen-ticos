from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from multiprocessing import Process
from Infraestructure.Logger import Logger


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = '/RPC2'


def av_carga_horaria(lista_cromossomos, lista_cursos):
    logger = Logger('RPCServer')
    logger.info('Iniciando a avaliação da lista de cromossomos pela carga horária dos cursos.')
    for i in range(len(lista_cromossomos)):
        cromossomos = lista_cromossomos[i]
        logger.info('Verificando os cromossomos do curso: ' + lista_cursos[i].nome)
        for j, cromossomo in enumerate(cromossomos):
            desconto = 0
            cromossome_list = cromossomo.cromossome
            # logger.info('Verificando o cromossomo {}'.format(j + 1))
            disciplinas = lista_cursos[i].lista_disciplinas
            for disciplina in disciplinas:
                id = disciplina.id
                qtd_aulas = disciplina.carga_horaria / 40
                qtd_ocorrencia = cromossome_list.count(id)
                desconto += abs(qtd_aulas - qtd_ocorrencia)
            desconto = desconto / 2
            cromossomo.nota = desconto
        logger.info('Finalizando a verificação dos cromossomos do curso: ' + lista_cursos[i].nome)
    logger.info('Finalizando a avaliação da lista de cromossomos pela carga horária dos cursos.')
    return lista_cromossomos


def av_choque_horario(lista_cromossomos, lista_disciplinas, lista_cursos):
    logger = Logger('RPCServer')
    logger.info('Iniciando a avaliação da lista de cromossomos verificando choques de horário.')
    for i in range(len(lista_cromossomos)):
        cromossomos = lista_cromossomos[i]
        logger.info('Verificando os cromossomos do curso: ' + lista_cursos[i].nome)
        for j, cromossomo in enumerate(cromossomos):
            choques = 0
            cromossome_list = cromossomo.cromossome
            # logger.info('Verificando o cromossomo {}'.format(j + 1))

            for k, position in enumerate(cromossome_list):
                cromossome_professor = get_professor_by_id(lista_disciplinas, position)
                for m in range(len(lista_cromossomos)):
                    if m != i:  # Evita comparar o mesmo curso
                        cromossomos_analysis = lista_cromossomos[m]
                        for n, cromossomo_analysis in enumerate(cromossomos_analysis):
                            cromossomo_analysis_list = cromossomo_analysis.cromossome
                            if len(cromossomo_analysis_list) > k and len(cromossome_list) > k:
                                nome_comparacao = get_professor_by_id(lista_disciplinas,
                                                                           cromossomo_analysis_list[k])
                                if cromossome_professor == nome_comparacao:
                                    choques += 1
            desconto = choques * 5
            cromossomo.nota = cromossomo.nota + desconto
        logger.info('Finalizando a verificação dos cromossomos do curso: ' + lista_cursos[i].nome)
        logger.info('Finalizando a avaliação da lista de cromossomos verificando choques de horário.')
    return lista_cromossomos


def av_disponibilidade(lista_cromossomos, lista_disponibilidade, lista_disciplinas, lista_cursos):
    logger = Logger('RPCServer')
    logger.info('Iniciando a avaliação da lista de cromossomos verificando a disponibilidade dos professores')
    for i in range(len(lista_cromossomos)):
        cromossomos = lista_cromossomos[i]
        logger.info('Verificando os cromossomos do curso: ' + lista_cursos[i].nome)
        for j, cromossomo in enumerate(cromossomos):
            indisponibilidade = 0
            cromossome_list = cromossomo.cromossome
            # logger.info('Verificando o cromossomo {}'.format(j + 1))

            for k, position in enumerate(cromossome_list):
                cromossome_professor = get_professor_by_id(lista_disciplinas, position)
                disponibilidade_professor = get_disponibilidade_by_nome(lista_disponibilidade, cromossome_professor)
                status = verifica_disponibilidade(disponibilidade_professor, len(cromossome_list), position)
                if status:
                    indisponibilidade += 1

            desconto = indisponibilidade * 3
            cromossomo.nota = cromossomo.nota + desconto
        logger.info('Finalizando a verificação dos cromossomos do curso: ' + lista_cursos[i].nome)
    logger.info('Finalizando a avaliação da lista de cromossomos verificando disponibilidade dos professores')
    return lista_cromossomos


def get_professor_by_id(lista_completa, id):
    for disciplina in lista_completa:
        if disciplina.id == id:
            return disciplina.professor
    return None


def get_disponibilidade_by_nome(lista_completa, nome):
    for disponibilidade in lista_completa:
        if disponibilidade.nome == nome:
            return disponibilidade
    return None


def mapear_para_dia_semana(numero, intervalo_maximo):
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

    # Mapear para os dias da semana
    dia_semana_idx = numero % len(dias_semana)
    dia_semana = dias_semana[dia_semana_idx]

    # Se o intervalo máximo for menor do que 5, ajustar para terça a sexta
    if intervalo_maximo < 5:
        dias_semana = ["Terça", "Quarta", "Quinta", "Sexta"]
        dia_semana = dias_semana[dia_semana_idx]

    return dia_semana


def verifica_disponibilidade(self, disponibilidade, numero, id_disciplina):
    dia_semana = self.mapear_para_dia_semana(numero, id_disciplina)

    # Use um dicionário para mapear os dias da semana para os atributos correspondentes em 'disponibilidade'
    dias_semana_dict = {'Segunda': 'segunda', 'Terça': 'terca', 'Quarta': 'quarta', 'Quinta': 'quinta',
                        'Sexta': 'sexta'}

    # Verifique a disponibilidade para o dia da semana correspondente
    if dia_semana in dias_semana_dict:
        atributo_dia_semana = dias_semana_dict[dia_semana]
        disponibilidade_dia = getattr(disponibilidade, atributo_dia_semana)

        # Se a disponibilidade para o dia da semana é 'N', então não está disponível
        if disponibilidade_dia == 'N':
            return False

    # Se nenhum bloqueio for encontrado, a disponibilidade é confirmada
    return True


class ProcessXMLRPCServer(Process):
    def run(self):
        print("Running RPC Server...")
        server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler)
        print("\tRegistering function Carga Horária...")
        server.register_function(av_carga_horaria)
        print("\tRegistering function Choque Horário...")
        server.register_function(av_choque_horario)
        print("\tRegistering function Disponibilidade...")
        server.register_function(av_disponibilidade)
        print("\tWaiting requests...")
        server.serve_forever()


if __name__ == "__main__":
    process_server = ProcessXMLRPCServer()
    process_server.start()
    process_server.join()

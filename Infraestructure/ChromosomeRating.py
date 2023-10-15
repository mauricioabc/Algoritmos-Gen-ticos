from Infraestructure.Logger import Logger


class ChromosomeRating:

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    def av_carga_horaria(self, lista_cromossomos, lista_cursos):
        self.logger.info('Iniciando a avaliação da lista de cromossomos pela carga horária dos cursos.')
        for i in range(len(lista_cromossomos)):
            cromossomos = lista_cromossomos[i]
            # self.logger.info('Verificando os cromossomos do curso: ' + lista_cursos[i].nome)
            for j, cromossomo in enumerate(cromossomos):
                desconto = 0
                cromossome_list = cromossomo.cromossome
                # self.logger.info('Verificando o cromossomo {}'.format(j + 1))
                disciplinas = lista_cursos[i].lista_disciplinas
                for disciplina in disciplinas:
                    id = disciplina.id
                    qtd_aulas = disciplina.carga_horaria / 40
                    qtd_ocorrencia = cromossome_list.count(id)
                    desconto += abs(qtd_aulas - qtd_ocorrencia)
                desconto = desconto / 2
                cromossomo.nota = desconto
            # self.logger.info('Finalizando a verificação dos cromossomos do curso: ' + lista_cursos[i].nome)
        self.logger.info('Finalizando a avaliação da lista de cromossomos pela carga horária dos cursos.')
        return lista_cromossomos

    def av_choque_horario(self, lista_cromossomos, lista_todos_cromossomos, lista_disciplinas, lista_cursos):
        self.logger.info('Iniciando a avaliação da lista de cromossomos verificando choques de horário.')

        # Criar conjunto de horários ocupados para cada curso
        horarios_ocupados_por_curso = [set() for _ in range(len(lista_cursos))]

        # Preencher conjuntos com horários ocupados
        for i, cromossomos in enumerate(lista_todos_cromossomos):
            for cromossomo in cromossomos:
                for position in cromossomo.cromossome:
                    professor = self.get_professor_by_id(lista_disciplinas, position)
                    horarios_ocupados_por_curso[i].add(professor)

        # Verificar choques de horário
        for i, cromossomos in enumerate(lista_cromossomos):
            for cromossomo in cromossomos:
                choques = sum(1 for position in cromossomo.cromossome if any(
                    professor in horarios_ocupados_por_curso[j] for j in range(len(lista_cursos)) if j != i
                ))
                desconto = choques * 5
                cromossomo.nota += desconto

        self.logger.info('Finalizando a avaliação da lista de cromossomos verificando choques de horário.')
        return lista_cromossomos

    def av_disponibilidade(self, lista_cromossomos, lista_disponibilidade, lista_disciplinas, lista_cursos):
        self.logger.info('Iniciando a avaliação da lista de cromossomos verificando a disponibilidade dos professores')
        for i in range(len(lista_cromossomos)):
            cromossomos = lista_cromossomos[i]
            # self.logger.info('Verificando os cromossomos do curso: ' + lista_cursos[i].nome)
            for j, cromossomo in enumerate(cromossomos):
                indisponibilidade = 0
                cromossome_list = cromossomo.cromossome
                # self.logger.info('Verificando o cromossomo {}'.format(j + 1))

                for k, position in enumerate(cromossome_list):
                    cromossome_professor = self.get_professor_by_id(lista_disciplinas, position)
                    disponibilidade_professor = self.get_disponibilidade_by_nome(lista_disponibilidade, cromossome_professor)
                    status = self.verifica_disponibilidade(disponibilidade_professor, len(cromossome_list), position)
                    if status:
                        indisponibilidade += 1

                desconto = indisponibilidade * 3
                cromossomo.nota = cromossomo.nota + desconto
            # self.logger.info('Finalizando a verificação dos cromossomos do curso: ' + lista_cursos[i].nome)
        self.logger.info('Finalizando a avaliação da lista de cromossomos verificando disponibilidade dos professores')
        return lista_cromossomos

    def get_professor_by_id(self, lista_completa, id):
        for disciplina in lista_completa:
            if disciplina.id == id:
                return disciplina.professor
        return None

    def get_disponibilidade_by_nome(self, lista_completa, nome):
        for disponibilidade in lista_completa:
            if disponibilidade.nome == nome:
                return disponibilidade
        return None

    def mapear_para_dia_semana(self, numero, intervalo_maximo):
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


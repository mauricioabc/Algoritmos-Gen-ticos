import json
from Infraestructure.Logger import Logger
from Entities.Curso import Curso
from Entities.Disciplina import Disciplina
from Entities.Disponibilidade import Disponibilidade


class Parser:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    def process_configs(self):
        self.logger.info('Iniciando o processamento dos arquivos de configuração.')
        try:
            lista_cursos = self.process_cursos()
            lista_disponibilidade = self.process_disponibilidade()
            lista_disciplinas = self.process_disciplinas(lista_cursos)
            self.logger.info('Processamento dos arquivos de configuração concluído com sucesso.')
            return lista_cursos, lista_disponibilidade, lista_disciplinas
        except Exception as e:
            self.logger.error('Ocorreu um erro inesperado: ' + str(e))

    def process_disciplinas(self, lista_cursos):
        lista_todas_disciplinas = []
        for curso in lista_cursos:
            disciplinas = curso.lista_disciplinas
            for disciplina in disciplinas:
                lista_todas_disciplinas.append(disciplina)
        return lista_todas_disciplinas

    def process_cursos(self):
        self.logger.info('Processando o arquivo de cursos e disciplinas.')
        try:
            filePath = '.\\Config\\cursos.json'
            with open(filePath, 'r', encoding='utf-8') as file:
                cursos_data = json.load(file)
            lista_cursos = []
            cursos = cursos_data['cursos']
            for curso in cursos:
                nome_curso = curso['nome']
                turno = curso['turno']
                dia_inicio = curso['dia_inicio']
                dia_fim = curso['dia_fim']
                novo_curso = Curso(nome_curso, turno, dia_inicio, dia_fim)
                disciplinas = curso['disciplinas']
                for disciplina in disciplinas:
                    nome_disciplina = disciplina['nome']
                    fase = disciplina['fase']
                    cargar_horaria = disciplina['carga_horaria']
                    professor = disciplina['professor']
                    disciplina = Disciplina(nome_disciplina, fase, cargar_horaria, professor)
                    novo_curso.adicionar_disciplina(disciplina=disciplina)
                lista_cursos.append(novo_curso)
            self.logger.info('Arquivo de cursos e disciplinas processado com sucesso.')
            return lista_cursos
        except Exception as e:
            self.logger.error('Ocorreu um erro inesperado: ' + str(e))

    def process_disponibilidade(self):
        self.logger.info('Processando o arquivo de disponibilidade dos professores.')
        try:
            filePath = '.\\Config\\disponibilidade.json'
            with open(filePath, 'r', encoding='utf-8') as file:
                disponibilidade_data = json.load(file)
            lista_disponibilidade = []
            professores = disponibilidade_data['professores']
            for professor in professores:
                nome = professor['nome']
                segunda = professor['segunda']
                terca = professor['terca']
                quarta = professor['quarta']
                quinta = professor['quinta']
                sexta = professor['sexta']
                novo_professor = Disponibilidade(nome, segunda, terca, quarta, quinta, sexta)
                lista_disponibilidade.append(novo_professor)
            self.logger.info('Arquivo de disponibilidade dos professores processado com sucesso.')
            return lista_disponibilidade
        except Exception as e:
            self.logger.error('Ocorreu um erro inesperado: ' + str(e))

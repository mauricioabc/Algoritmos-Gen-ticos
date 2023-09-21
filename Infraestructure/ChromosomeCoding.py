from Infraestructure.Logger import Logger
from Infraestructure.RandomNumber import RandomNumber


class ChromosomeCoding:
    def __init__(self, tamanho_populacao):
        self.logger = Logger(self.__class__.__name__)
        self.random = RandomNumber()
        self.tamanho_populacao = tamanho_populacao

    def process_initial_chromosomes(self, lista_cursos):
        self.logger.info('Iniciando a modelagem do problema.')
        try:
            lista_cromossomos = []
            for curso in lista_cursos:
                cromossomos_curso = self.chromosomes_generate(curso, self.tamanho_populacao)
                lista_cromossomos.append(cromossomos_curso)
            self.logger.info('Modelagem do problema concluída com sucesso.')
            return lista_cromossomos
        except Exception as e:
            self.logger.error('Ocorreu um erro inesperado: ' + str(e))

    def chromosomes_generate(self, curso, tamanho_populacao):
        self.logger.info('Iniciando criação de cromossomos para o curso: ' + curso.nome)
        try:
            lista_fases = set()
            lista_disciplinas = curso.lista_disciplinas
            for disciplina in curso.lista_disciplinas:
                fase = disciplina.fase
                lista_fases.add(fase)
            lista_fases = sorted(list(lista_fases))
            cromossomos = []
            cromossomo = []
            quantidade_dias = curso.getNumeroDias()
            quantidade_aulas = 2
            tamanho_max_cromossomo = len(lista_fases) * quantidade_dias * quantidade_aulas
            tamanho_cromossomo = quantidade_dias * 2
            for i in range(tamanho_populacao):
                for fase in lista_fases:
                    disciplinas_organizadas = self.disciplinas_por_fase(lista_disciplinas, fase)
                    inicio, fim = self.range_id_disciplinas(disciplinas_organizadas)
                    for k in range(tamanho_cromossomo):
                        valor = self.random.random_number_generator(inicio, fim)
                        if len(cromossomo) == tamanho_max_cromossomo:
                            cromossomos.append(cromossomo)
                            cromossomo = []
                        else:
                            cromossomo.append(valor)
            self.logger.info('Criação de cromossomos concluída com sucesso para o curso: ' + curso.nome)
            return cromossomos
        except Exception as e:
            self.logger.error('Ocorreu um erro inesperado: ' + str(e))

    def disciplinas_por_fase(self, lista_disciplinas, fase):
        disciplinas_organizadas = []
        for disciplina in lista_disciplinas:
            if disciplina.fase == fase:
                disciplinas_organizadas.append(disciplina)
        return disciplinas_organizadas

    def range_id_disciplinas(self, lista_disciplinas):
        inicio = lista_disciplinas[0].id
        fim = lista_disciplinas[len(lista_disciplinas) - 1].id
        return inicio, fim
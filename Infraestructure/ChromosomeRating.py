class ChromosomeRating:
    def av_carga_horaria(lista_cromossomos, lista_disciplinas, lista_cursos):
        desconto = 0
        for i in range(len(lista_cromossomos)):
            cromossomos = lista_cromossomos[i]
            # tamanho_fase = len(cromossomo)/4
            # lista_fases = []
            # inicio_corte = 0
            # fim_corte = -1
            # for j in range(4):
            #     fim_corte += tamanho_fase
            #     lista_fases.append(cromossomo[int(inicio_corte):int(fim_corte)])
            for cromossomo in cromossomos:
                disciplinas = lista_cursos[i].lista_disciplinas
                for disciplina in disciplinas:
                    id = disciplina.id
                    qtd_ocorrencia = 0
                    qtd_aulas = disciplina.carga_horaria/40
                    qtd_ocorrencia =cromossomo.count(id)
                    desconto += abs(qtd_aulas - qtd_ocorrencia)
        return (desconto/2)*10

    def av_choque_horario(lista_cromossomos):
        choques = 0
    #em obras
        return choques



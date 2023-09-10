from Infraestructure.Parser import Parser


def main():
    # Busca e internaliza os dados dos professores e turmas
    parser = Parser()
    lista_cursos, lista_disponibilidade = parser.process_configs()
    print(str(len(lista_cursos)) + ' - ' + str(len(lista_disponibilidade)))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

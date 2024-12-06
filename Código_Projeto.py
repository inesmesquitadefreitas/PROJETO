# PROJETO

# !!! No projeto, temos de editar o ficheiro do stor "Dados_Projeto.json" (não sabemos fazer isso) --> definimos uma variável "publicacoes" para simular esse ficheiro

# 1) CARREGAMENTO DA BASE DE DADOS: O programa no arranque deverá carregar para memória o dataset que deverá estar guardado no ficheiro de suporte à aplicação

import json

f = open(r"C:\Users\Inês Mesquita\Documents\Eng_Biomédica\Programação\Projeto\Dados_Projeto.json", encoding='utf-8') # Abre o arquivo Dados_Projeto.json, que possui o path "C:\Users\Inês Mesquita\Documents\Eng_Biomédica\Programação\Projeto\" | # encoding='utf-8' garante que o arquivo seja lido corretamente, especialmente se tiver caracteres especiais
aceder_dados = json.load(f) # Lê o conteúdo do arquivo JSON e transforma-o numa estrutura de dados Python. Geralmente, o JSON é carregado como listas ou dicionários (dependendo da estrutura do arquivo). Aqui, o conteúdo é atribuído à variável "dados"

def carregaDADOS(fnome): # Define a função carregaDADOS, que aceita um argumento "fnome" (=nome de um arquivo JSON) e carrega o seu conteúdo.
    f = open(r"C:\Users\Inês Mesquita\Documents\Eng_Biomédica\Programação\Projeto\Dados_Projeto.json", encoding='utf-8') # Abre o arquivo Dados_Projeto.json com o path indicado anteriormente.
    carrega_dados = json.load(f) # Lê e carrega os dados do arquivo JSON na variável "carrega_dados"
    return carrega_dados

dados = carregaDADOS("Dados_Projeto.json") # Chama a função carregaDADOS, passando "Dados_Projeto.json" como argumento.

# --------------------------------------------------------------------------------------------------------------------------

# 2) CRIAÇÃO DE PUBLICAÇÕES: O utilizador deve poder criar um artigo especificando um título, resumo, palavras-chave, DOI, uma lista de autores e sua afiliação correspondente, url para o ficheiro PDF do artigo, data de publicação e url do artigo;

def criarPublicacao(): 

    print(" -------- NOVA PUBLICAÇÃO --------")

    # Input dos dados necessários para cada chave

    titulo = input("Título do artigo: ").strip() # .strip() --> remover espaços em branco no início e no fim de uma string (ou outros caracteres especificados)
    resumo = input("Resumo do artigo: ").strip()
    palavras_chave = input("Palavras-chave (separadas por vírgula): ").strip().split(",") # split(",") --> fatiar a string pela vírgula, obtendo cada uma das palavras-chave 
    doi = input("DOI: ").strip()

    autores = []
    cond = True
    while cond:
        nome_autor = input("Nome do autor: ").strip()
        if nome_autor == "":
            cond = False
        else:
            autor_afiliacao = input(f"Afiliação do autor {nome_autor}': ").strip()
            autores.append({"Nome": nome_autor, "Afiliação": autor_afiliacao})


    url_pdf = input("URL do PDF: ").strip()
    url_artigo = input("URL do artigo: ").strip()

    data_publicacao = ""
    while data_publicacao == "":
        data_input = input("Data de Publicação (YYYY-MM-DD): ").strip()
        partes_data = data_input.split("-")
        if len(partes_data) == 3 and all(p.isdigit() for p in partes_data):
            ano, mes, dia = int(partes_data[0]), int(partes_data[1]), int(partes_data[2])
            if 1 <= mes <= 12 and 1 <= dia <= 31:  # Verificação básica
                if mes in [4, 6, 9, 11] and dia > 30:  # Meses com 30 dias
                    print("Mês especificado tem no máximo 30 dias.")
                elif mes == 2 and (dia > 29 or (dia == 29 and ano % 4 != 0)):  # Fevereiro
                    print("Data inválida em fevereiro.")
                else:
                    data_publicacao = f"{ano:04d}-{mes:02d}-{dia:02d}"
            else:
                print("Mês ou dia fora do intervalo.")
        else:
            print("Formato de data inválido. Use YYYY-MM-DD.")
    
    # Criar o dicionário da publicação

    nova_publicacao = {
        "Título": titulo,
        "Resumo": resumo,
        "Palavras-Chave": [palavra.strip() for palavra in palavras_chave],
        "DOI": doi,
        "Autores": autores,
        "URL do PDF": url_pdf,
        "Data da Publicação": data_publicacao,
        "URL do Artigo": url_artigo
    }
    

# !!! Não conseguimos adicionar a Publicação ao documento "Dados_Projeto.json"
def salvarDados(dados, ficheiro="Dados_Projeto.json"):
    # Abre o ficheiro e grava os dados em formato JSON
    f = open(ficheiro, "w", encoding="utf-8")
    f.write(json.dumps(dados, f, indent=4))
    f.close()
    print(f"Dados salvos com sucesso no ficheiro {ficheiro}!")

# --------------------------------------------------------------------------------------------------------------------------

# 3) ATUALIZAÇÃO DE PUBLICAÇÕES: O sistema deve permitir a atualização da informação de uma publicação, nomeadamente a data de publicação, o resumo, palavras-chave, autores e afiliações;

def atualizarPublicacao(publicacoes, indice):
    if 0 <= indice < len(publicacoes):
        publicacao = publicacoes[indice]
        print(f"Atualizando a publicação: {publicacao["Título"]}")

    # Atualizar título
    titulo = input(f"Novo título (atual: {publicacao["Título"]}): ").strip() or publicacao["Título"]
    publicacao["Título"] = titulo
        
    # Atualizar resumo
    resumo = input(f"Novo resumo (atual: {publicacao["Resumo"]}): ").strip() or publicacao["Resumo"]
    publicacao["Resumo"] = resumo

    # Atualizar palavras-chave
    palavras_chave = input(f"Novas palavras-chave (atual: {publicacao["Palavras-Chave"]}): ").strip() or publicacao["Palavras-Chave"]
    publicacao["Palavras-Chave"] = palavras_chave

    # Atualizar autores e afiliações
    for autor in publicacao["Autores"]:
        autor["Nome"] = input(f"Novo nome para o autor '{autor["Nome"]}' (deixe em branco para não alterar): ").strip() or autor["Nome"]
        autor["Afiliação"] = input(f"Nova afiliação para o autor '{autor["Nome"]}' (deixe em branco para não alterar): ").strip() or autor["Afiliação"]
    
    # Atualizar data de publicação
    nova_data = input(f"Nova data de publicação (atual: {publicacao["Data da Publicação"]}): ").strip() # Exemplo: nova_data_input = 2024-01-01
    partes = nova_data.split("-") # partes = ['01', '01', '2024']
    if len(partes) == 3 and all(p.isdigit() for p in partes): # verificar se len(partes) == 3 --> verificar se partes possui "ano", "mês" e "dia" E verificar se "for p in partes", all(p.isdigit() --> se cada elemento de "ano", "mês" e "dia" é um dígito
        ano, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
        if 1 <= mes <= 12 and 1 <= dia <= 31:  # Verificação básica
            if mes in [4, 6, 9, 11] and dia > 30:  # Meses com 30 dias
                print("Mês especificado tem no máximo 30 dias.")
            elif mes == 2 and (dia > 29 or (dia == 29 and ano % 4 != 0)): # Fevereiro
                    print("Data inválida em fevereiro.")
            else:
                publicacao["Data da Publicação"] = f"{ano:04d}-{mes:02d}-{dia:02d}" # 04d: 4 dígitos // 02d: 2 dígitos

            print("Publicação atualizada com sucesso!")
        else:
            print("Erro: Índice da publicação inválido!")

# --------------------------------------------------------------------------------------------------------------------------

# 4. CONSULTA DE PUBLICAÇÕES: O sistema deve permitir pesquisar publicações. Esta pesquisa deve permitir filtros por título, autor, afiliação, data de publicação e palavras-chave. Deve ainda ser possível ordenar as publicações encontradas pelos títulos e pela data de publicação;

def consultarPublicacoes(publicacoes): # publicacoes é o documento "Dados_Projeto.json" --> como o identifico?
    
    # O utilizador vai selecionar o tipo de filtro que vai usar para pesquisar publicações
    print("--- CONSULTA DE PUBLICAÇÕES ---")
    print("1. Título")
    print("2. Autor")
    print("3. Afiliação")
    print("4. Data de Publicação")
    print("5. Palavra-chave")
    
    opcao = input("Selecione o tipo de filtro (1-5): ").strip()

    if opcao == "1":
        filtro = input("Digite o título: ").strip().lower()
        chave_filtro = "Título"
    elif opcao == "2":
        filtro = input("Digite o nome do autor: ").strip().lower()
        chave_filtro = "Autor"
    elif opcao == "3":
        filtro = input("Digite a afiliação: ").strip().lower()
        chave_filtro = "Afiliação"
    elif opcao == "4":
        filtro = input("Digite a data de publicação (YYYY-MM-DD): ").strip()
        chave_filtro = "Data da Publicação"
    elif opcao == "5":
        filtro = input("Digite a palavra-chave: ").strip().lower()
        chave_filtro = "Palavras-Chave"
    else:
        print("Opção inválida!")
        return

    # Filtrar publicações com base no critério escolhido
    publicacoes_encontradas = []
    for p in publicacoes:
        if chave_filtro == "Título" and filtro in p["Título"].lower():
            publicacoes_encontradas.append(p)
        elif chave_filtro == "Autor":
            for autor in p["Autores"]:
                if filtro in autor["Nome"].lower():
                    publicacoes_encontradas.append(p)
        elif chave_filtro == "Afiliação":
            for autor in p["Autores"]:
                if filtro in autor["Afiliação"].lower():
                    publicacoes_encontradas.append(p)
        elif chave_filtro == "Data da Publicação" and p["Data da Publicação"] == filtro:
            publicacoes_encontradas.append(p)
        elif chave_filtro == "Palavras-Chave":
            for palavra in p["Palavras-Chave"]:
                if filtro in palavra.lower():
                   publicacoes_encontradas.append(p)
    

    # Ordenar os resultados por data e título
    publicacoes_encontradas.sort(key=lambda x: (x["Data da Publicação"], x["Título"].lower())) # sort: modifica a lista original
    
    # Exibir os resultados
    if publicacoes_encontradas != []:
        print("--- RESULTADOS DA PESQUISA ---")
        for i, p in enumerate(publicacoes_encontradas, start=1):
            print(f"{i}) Título: {p['Título']}")
            print(f"   Data da Publicação: {p['Data da Publicação']}")
            print(f"   Autores: {', '.join(autor['Nome'] for autor in p['Autores'])}")
            print(f"   DOI: {p['DOI']}")
            print(f"   Palavras-Chave: {', '.join(p['Palavras-Chave'])}")
    else:
        print("Nenhuma publicação encontrada com o critério especificado.")
    
    return publicacoes_encontradas

# --------------------------------------------------------------------------------------------------------------------------

# 5. ANÁLISE DE PUBLICAÇÕES POR AUTOR: O sistema deve permitir listar os autores e aceder aos artigos de cada autor da lista. Os autores devem aparecer ordenados pela frequência dos seus artigos publicados e/ou por ordem alfabética;

def analisePorAutor(publicacoes):
    
    # Dicionário para armazenar os autores e as suas publicações
    dicionario_autores = {}

    # Contar publicações de cada autor
    for p in publicacoes:
        for autor in p["Autores"]:
            nome_autor = autor["Nome"]
            if nome_autor not in dicionario_autores:
                dicionario_autores[nome_autor] = [] # se o nome do autor não for uma chave no dicionario_autores, inseri-lo como chave com o valor de uma lista vazia
            dicionario_autores[nome_autor].append(p) # se ele já for chave, adicionar a publicação p à lista de publicações do autor

    # Perguntar ao utilizador o tipo de ordenação
    print("--- ANÁLISE DE PUBLICAÇÕES POR AUTOR ---")
    print("1. Ordenar por frequência de artigos publicados (ordem decrescente).")
    print("2. Ordenar por ordem alfabética dos nomes dos autores.")
    opcao = input("Escolha o tipo de ordenação (1/2): ").strip()

    if opcao == "1":
        autores_ordenados = sorted(dicionario_autores.items(), key=lambda x: len(x[1]), reverse=True)
    elif opcao == "2":
        autores_ordenados = sorted(dicionario_autores.items(), key=lambda x: x[0].lower())
    else:
        print("Opção inválida! Exibindo autores em ordem aleatória.")
        autores_ordenados = dicionario_autores.items()

    print("--- RESULTADOS ---")
    for autor, artigos in autores_ordenados:
        print(f"Autor: {autor}: ({len(artigos)} artigos publicados)")
        for i, p in enumerate(artigos, start=1):
            print(f"{i}. {p['Título']} (Publicado em {p['Data da Publicação']})")

    return dict(autores_ordenados)

# --------------------------------------------------------------------------------------------------------------------------

# 6. ANÁLISE DE PUBLICAÇÕES POR PALAVRA-CHAVE: O sistema deve permitir a pesquisa e visualização das palavras-chave do dataset. As palavras-chave devem estar ordenadas pelo seu número de ocorrências nos artigos e/ou por ordem alfabética. O sistema deve também permitir visualizar a lista das publicações associadas a cada palavra-chave;

def analisePorPalavraChave(publicacoes):
    
    # Dicionário para contar palavras-chave e associar as publicações
    dicionario_palavras = {}

    for p in publicacoes:
        for palavra in p["Palavras-Chave"]:
            palavra = palavra.lower()
            if palavra not in dicionario_palavras:
                dicionario_palavras[palavra] = []
            dicionario_palavras[palavra].append(p)

    print("--- ANÁLISE DE PUBLICAÇÕES POR PALAVRA-CHAVE ---")
    print("1. Ordenar palavras-chave pela frequência de ocorrências (ordem decrescente).")
    print("2. Ordenar palavras-chave por ordem alfabética.")
    opcao = input("Escolha o tipo de ordenação (1/2): ").strip()

    if opcao == "1":
        palavras_ordenadas = sorted(dicionario_palavras.items(), key=lambda x: len(x[1]), reverse=True)
    elif opcao == "2":
        palavras_ordenadas = sorted(dicionario_palavras.items(), key=lambda x: x[0])
    else:
        print("Opção inválida! Exibindo palavras-chave em ordem aleatória.")
        palavras_ordenadas = dicionario_palavras.items()

    print("--- RESULTADOS ---")
    for palavra, artigos in palavras_ordenadas:
        print(f"Palavra-chave: '{palavra}': ({len(artigos)} ocorrências)")
        for i, p in enumerate(artigos, start=1):
            print(f"{i}. {p['Título']} (Publicado em {p['Data da Publicação']})")



# --------------------------------------------------------------------------------------------------------------------------

# 7. ESTATÍSTICAS DE PUBLICAÇÃO: O sistema deve apresentar relatórios que incluam os seguintes gráficos:

import matplotlib.pyplot as plt

# - Distribuição de publicações por ano:

def distPublicacoesPorAno(publicacoes):
    contagem_anos = {}
    for publicacao in publicacoes:
        ano = int(publicacao["Data da Publicação"].split("-")[0])  # Extrair o 1º elemento da lista resultante, se fatiarmos a data pelo "-" = ano
        if ano not in contagem_anos:
            contagem_anos[ano] = 1
        else:
            contagem_anos[ano] = contagem_anos[ano] + 1

    # - Converte o dicionário "anos_ordenados" numa lista de tuplos (ano, nº de publicações)
    # - Ordena os tuplos com base no seu 1º elemento = ano
    anos_ordenados = sorted(contagem_anos.items(), key=lambda x: x[0])
    for x in anos_ordenados:
        ano, contagem_publicacoes = x

    # Gráfico
    plt.bar(ano, contagem_publicacoes, color="skyblue")
    plt.xlabel("Ano")
    plt.ylabel("Número de Publicações")
    plt.title("Distribuição de Publicações por Ano")
    plt.show()


# - Distribuição de publicações por mês de um determinado ano:

def distPublicacoesPorMes(publicacoes, ano_escolhido):
    # Contar publicações por mês no ano escolhido
    contagem_meses = {mes: 0 for mes in range(1, 13)} # dicionário em compreensão --> criar um dicionário que tenha como chave todos os números de 1 até 12 (meses) e o respetivos valores começam a zero
    # contagem_meses = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0 }

    for p in publicacoes:
        ano, mes, _ = map(int, p["Data da Publicação"].split("-")) # map --> aplica a função int a cada elemento da lista resultante de p["Data da Publicação"].split("-")
        if ano == ano_escolhido:
            contagem_meses[mes] = contagem_meses[mes] + 1

    # Gráfico
    meses = list(contagem_meses.keys())
    numero_publicacoes = list(contagem_meses.values())

    plt.bar(meses, numero_publicacoes, color="lightgreen")
    plt.xlabel("Mês")
    plt.ylabel("Número de Publicações")
    plt.title(f"Distribuição de Publicações por Mês em {ano_escolhido}")
    plt.xticks(meses) # ???
    plt.show()


# - Número de publicações por autor (top 20 autores):

def distPublicacoesPorAutor(publicacoes):
    contagem_autores = {}
    for p in publicacoes:
        for autor in p["Autores"]:
            nome = autor["Nome"]
            if nome not in contagem_autores:
                contagem_autores[nome] = 1
            else:
                contagem_autores[nome] = contagem_autores[nome] + 1

    autores_ordenados = sorted(contagem_autores.items(), key=lambda x: x[1], reverse=True)
    top20_autores = autores_ordenados[:20]
    for y in top20_autores:
        nomes, n_publicacoes = y

    # Gráfico
    plt.barh(nomes, n_publicacoes, color="pink")
    plt.xlabel("Número de Publicações")
    plt.ylabel("Autores")
    plt.title("Top 20 Autores por Número de Publicações")
    plt.gca().invert_yaxis()  # Inverte para o maior no topo # ??????????
    plt.show()


# - Distribuição de publicações de um autor por anos:

def distPublicacoesAutorPorAnos(publicacoes, nome_autor):
    contagem_anos = {}
    for p in publicacoes:
        ano = int(p["Data da Publicação"].split("-")[0])
        for autor in p["Autores"]:
            if autor["Nome"].lower() == nome_autor.lower():
                if ano not in contagem_anos:
                    contagem_anos[ano] = 1
                else:
                    contagem_anos[ano] = contagem_anos[ano] + 1

    anos_ordenados = sorted(contagem_anos.items(), key=lambda x: x[0])
    for z in anos_ordenados:
        anos, quantidades = z

    # Gráfico
    plt.bar(anos, quantidades, color="purple")
    plt.xlabel("Ano")
    plt.ylabel("Número de Publicações")
    plt.title(f"Distribuição de Publicações de {nome_autor} por Anos")
    plt.show()


# - Distribuição de palavras-chave pela sua frequência (top 20 palavras-chave):

def distPalavrasChavePorFrequencia(publicacoes):
    contagem_palavras = {}
    for p in publicacoes:
        for palavra in p["Palavras-Chave"]:
            palavra = palavra.lower()
            if palavra not in contagem_palavras:
                contagem_palavras[palavra] = 1
            contagem_palavras[palavra] = contagem_palavras[palavra] + 1

    palavras_ordenadas = sorted(contagem_palavras.items(), key=lambda x: x[1], reverse=True)
    top20_palavras = palavras_ordenadas[:20]
    for w in top20_palavras:
        palavra, frequencia = w

    # Gráfico
    plt.barh(palavra, frequencia, color="red") # ???
    plt.xlabel("Frequência")
    plt.ylabel("Palavras-Chave")
    plt.title("Top 20 Palavras-Chave por Frequência")
    plt.gca().invert_yaxis()  # Inverte para a mais frequente no topo # ?????
    plt.show()
    
# - Distribuição de palavras-chave mais frequente por ano.

# 8. ARMAZENAMENTO DOS DADOS: Quando o utilizador decidir sair da aplicação ou tiver selecionado o armazenamento dos dados, a aplicação deverá guardar os dados em memória no ficheiro de suporte;

# 9. IMPORTAÇÃO DE DADOS: Em qualquer momento, deverá ser possível importar novos registos dum outro ficheiro que tenha a mesma estrutura do ficheiro de suporte;

# 10. EXPORTAÇÃO PARCIAL DE DADOS: Em qualquer momento, deverá ser possível exportar para ficheiro os registos resultantes de uma pesquisa (apenas o subconjunto retornado pela pesquisa).

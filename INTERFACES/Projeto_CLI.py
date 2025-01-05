import json

# ----------------------------------------------------------------------
# Carregar dados do arquivo JSON
def carregaDADOS(fnome):
    with open(fnome, encoding='utf-8') as f:
        return json.load(f)

# Salvar dados no arquivo JSON
def salvarDados(dados, ficheiro="ataMedicaPapers.json"):
    try:
        with open(ficheiro, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
            print(f"Dados salvos com sucesso no ficheiro {ficheiro}!")
    except Exception as e:
        print(f"Erro ao salvar dados no ficheiro {ficheiro}: {e}")

# Carregar dados no início do programa
dados = carregaDADOS("C:/Users/Inês Mesquita/Documents/Eng_Biomédica/Programação/Projeto/ataMedicaPapers.json")
# ----------------------------------------------------------------------
# (1) Função para CRIAR uma nova publicação
def criarPublicacao():
    print("\n-------- NOVA PUBLICAÇÃO --------")
    titulo = input("Título do artigo: ").strip() # strip() --> remover caracteres especificados (neste caso, o \n e espaços em branco no início e fim de uma string)
    resumo = input("Resumo do artigo: ").strip()
    palavras_chave = input("Palavras-chave (separadas por vírgulas): ").strip(". ")
    doi = input("DOI: ").strip()
    url_pdf = input("URL do PDF: ").strip()
    url_artigo = input("URL do artigo: ").strip()

    autores = []
    cond = True
    while cond:
        nome_autor = input("Nome do autor (deixe em branco para terminar): ").strip()
        if not nome_autor: # if nome_autor == "":
            cond = False
        autor_afiliacao = input(f"Afiliação do autor {nome_autor}: ").strip()
        if nome_autor and autor_afiliacao:
            autores.append({"name": nome_autor, "affiliation": autor_afiliacao})

    data_publicacao = ""
    while not data_publicacao: # while data_publicacao == "":
        data_input = input("Data de Publicação (YYYY-MM-DD): ").strip()
        partes_data = data_input.split("-")
        if len(partes_data) == 3 and all(p.isdigit() for p in partes_data):
            ano, mes, dia = int(partes_data[0]), int(partes_data[1]), int(partes_data[2])
            if 1 <= mes <= 12 and 1 <= dia <= 31:
                if mes in [4, 6, 9, 11] and dia > 30:
                    print("Mês especificado tem no máximo 30 dias.\n")
                elif mes == 2 and (dia > 29 or (dia == 29 and ano % 4 != 0)):
                    print("Data inválida em fevereiro.\n")
                else:
                    data_publicacao = f"{ano:04d}-{mes:02d}-{dia:02d}"
            else:
                print("Mês ou dia fora do intervalo.\n")
        else:
            print("Formato de data inválido. Use YYYY-MM-DD.\n")

    nova_publicacao = {
        "title": titulo,
        "abstract": resumo,
        "keywords": palavras_chave,
        "doi": doi,
        "authors": autores,
        "pdf": url_pdf,
        "publish_date": data_publicacao,
        "url": url_artigo
    }

    dados.append(nova_publicacao)
    salvarDados(dados)

# ----------------------------------------------------------------------
# (2) Função para CONSULTAR uma publicação específica
def consultarPublicacao(indice):
    if 0 <= indice < len(dados):
        publicacao = dados[indice]
        print(f"\n-------- PUBLICAÇÃO DE ÍNDICE {indice} --------\n")
        if publicacao.get('title'):
            print(f"Título: {publicacao['title']}\n")
        if publicacao.get('abstract'):
            print(f"Resumo: {publicacao['abstract']}\n")
        if publicacao.get('keywords'):
            listaKeywords = [palavra.strip(". ") for palavra in publicacao['keywords'].split(", ")]
            print(f"Palavras-Chave: {', '.join(listaKeywords)}\n")
        if publicacao.get('authors'):
            listaAutores = []
            for p in publicacao['authors']:
                nomeAutor = p.get('name')
                listaAutores.append(nomeAutor)
            print(f"Autores: {', '.join(listaAutores)}\n")
        if publicacao.get('doi'):
            print(f"DOI: {publicacao['doi']}\n")
        if publicacao.get('pdf'):
            print(f"URL do PDF: {publicacao['pdf']}\n")
        if publicacao.get('url'):
            print(f"URL do Artigo: {publicacao['url']}\n")
        if publicacao.get('publish_date'):
            print(f"Data da Publicação: {publicacao['publish_date']}\n")
    else:
        print("Erro: Índice da publicação inválido!\n")

# ----------------------------------------------------------------------
# (3) Função para FILTRAR publicações
def consultarPublicacoes():
    print("\n-------- CONSULTA DE PUBLICAÇÕES --------")
    print("1. Título")
    print("2. Autor")
    print("3. Afiliação")
    print("4. Data da Publicação")
    print("5. Palavra-chave")
    
    opcao = input("Selecione o tipo de filtro (1-5): ").strip()

    if opcao == "1":
        filtro = input("Digite o título: ").strip().lower()
        chave_filtro = "Título"
    elif opcao == "2":
        filtro = input("Digite o nome do autor: ").strip().lower()
        chave_filtro = "Nome do Autor"
    elif opcao == "3":
        filtro = input("Digite a afiliação: ").strip().lower()
        chave_filtro = "Afiliação"
    elif opcao == "4":
        filtro = input("Digite a data da publicação (YYYY-MM-DD): ").strip()
        chave_filtro = "Data da Publicação"
    elif opcao == "5":
        filtro = input("Digite a palavra-chave: ").strip().lower()
        chave_filtro = "Palavras-Chave"
    else:
        print("Opção inválida!\n")

    publicacoes_encontradas = []
    for p in dados:
        if chave_filtro == "Título": # p.get('title') --> pode have publicações sem a chave 'title' (prevenimos erros)
            if p.get('title'):
                if filtro.lower() in p['title'].lower() and p not in publicacoes_encontradas:
                    publicacoes_encontradas.append(p)
        elif chave_filtro == "Nome do Autor":
            for autor in p.get('authors'):
                if autor.get('name'):
                    if filtro.lower() in autor['name'].lower() and p not in publicacoes_encontradas:
                        publicacoes_encontradas.append(p)
        elif chave_filtro == "Afiliação":
            for autor in p.get("authors"):
                if autor.get('affiliation'):
                    if filtro.lower() in autor['affiliation'].lower() and p not in publicacoes_encontradas:
                        publicacoes_encontradas.append(p)
        elif chave_filtro == "Data da Publicação":
            if p.get('publish_date') == filtro and p not in publicacoes_encontradas:
                publicacoes_encontradas.append(p)
        elif chave_filtro == "Palavras-Chave":
            if p.get('keywords'):
                for palavra in p['keywords'].split(", "):
                    palavra = palavra.strip('. ')
                    if filtro in palavra.lower() and p not in publicacoes_encontradas:
                        publicacoes_encontradas.append(p)
    
    print("\n(1) Ordenar artigos por data de publicação (da mais recente à mais antiga)")
    print("(2) Ordenar artigos por ordem alfabética dos títulos")
    opcao = input("Escolha o tipo de ordenação (1/2): ").strip()

    if publicacoes_encontradas:
        if opcao == "1":
            sem_data = [p for p in publicacoes_encontradas if not p.get("publish_date")]
            com_data = [p for p in publicacoes_encontradas if p.get("publish_date")]

            if sem_data:
                print("\n---------- PUBLICAÇÕES SEM DATA ----------\n")
                for pub in sem_data:
                    if pub.get('title'):
                        print(f"Título: {pub['title']}")
                    if pub.get('keywords'):
                        listaKeywords = [palavra.strip(". ") for palavra in pub['keywords'].split(", ")]
                        print(f"Palavras-Chave: {', '.join(listaKeywords)}")
                    if pub.get('authors'):
                        listaAutores = []
                        listaAfiliacoes = []
                        for p in pub['authors']:
                            if p.get('name'):
                                nomeAutor = p['name']
                                listaAutores.append(nomeAutor)
                            if p.get('affiliation'):
                                afiliacaoAutor = p['affiliation']
                                if afiliacaoAutor not in listaAfiliacoes:
                                    listaAfiliacoes.append(afiliacaoAutor)
                        print(f"Autores: {', '.join(listaAutores)}")
                        print(f"Afiliações: {', '.join(listaAfiliacoes)}")
                    if pub.get('doi'):
                        print(f"DOI: {pub['doi']}")
                        print("\n")

            if com_data:
                com_data.sort(key=lambda x: x["publish_date"], reverse=True)
                print("\n---------- PUBLICAÇÕES COM DATA ORDENADAS ----------\n")
                for pub in com_data:
                    if pub.get('title'):
                        print(f"Título: {pub['title']}")
                    if pub.get('keywords'):
                        listaKeywords = [palavra.strip(". ") for palavra in pub['keywords'].split(", ")]
                        print(f"Palavras-Chave: {', '.join(listaKeywords)}")
                    if pub.get('authors'):
                        listaAutores = []
                        listaAfiliacoes = []
                        for p in pub['authors']:
                            if p.get('name'):
                                nomeAutor = p['name']
                                listaAutores.append(nomeAutor)
                            if p.get('affiliation'):
                                afiliacaoAutor = p['affiliation']
                                if afiliacaoAutor not in listaAfiliacoes:
                                    listaAfiliacoes.append(afiliacaoAutor)
                        print(f"Autores: {', '.join(listaAutores)}")
                        print(f"Afiliações: {', '.join(listaAfiliacoes)}")
                    if pub.get('doi'):
                        print(f"DOI: {pub['doi']}")
                    print(f"Data da Publicação: {pub['publish_date']}")
                    print("\n")

        elif opcao == "2":
            sem_titulo = [p for p in publicacoes_encontradas if not p.get("title")]
            com_titulo = [p for p in publicacoes_encontradas if p.get("title")]

            if sem_titulo:
                print("\n---------- PUBLICAÇÕES SEM TÍTULO ----------\n")
                for pub in sem_titulo:
                    if pub.get('keywords'):
                        listaKeywords = [palavra.strip(". ") for palavra in pub['keywords'].split(", ")]
                        print(f"Palavras-Chave: {', '.join(listaKeywords)}")
                    if pub.get('authors'):
                        listaAutores = []
                        listaAfiliacoes = []
                        for p in pub['authors']:
                            if p.get('name'):
                                nomeAutor = p['name']
                                listaAutores.append(nomeAutor)
                            if p.get('affiliation'):
                                afiliacaoAutor = p['affiliation']
                                if afiliacaoAutor not in listaAfiliacoes:
                                    listaAfiliacoes.append(afiliacaoAutor)
                        print(f"Autores: {', '.join(listaAutores)}")
                        print(f"Afiliações: {', '.join(listaAfiliacoes)}")
                    if pub.get('doi'):
                        print(f"DOI: {pub['doi']}")
                    if pub.get('publish_date'):
                        print(f"Data da Publicação: {pub['publish_date']}")
                    print("\n")

            if com_titulo:
                com_titulo.sort(key=lambda x: x["title"].lower())
                print("\n---------- PUBLICAÇÕES COM TÍTULO ORDENADAS ----------\n")
                for pub in com_titulo:
                    print(f"Título: {pub['title']}")
                    if pub.get('keywords'):
                        listaKeywords = [palavra.strip(". ") for palavra in pub['keywords'].split(", ")]
                        print(f"Palavras-Chave: {', '.join(listaKeywords)}")
                    if pub.get('authors'):
                        listaAutores = []
                        listaAfiliacoes = []
                        for p in pub['authors']:
                            if p.get('name'):
                                nomeAutor = p['name']
                                listaAutores.append(nomeAutor)
                            if p.get('affiliation'):
                                afiliacaoAutor = p['affiliation']
                                if afiliacaoAutor not in listaAfiliacoes:
                                    listaAfiliacoes.append(afiliacaoAutor)
                        print(f"Autores: {', '.join(listaAutores)}")
                        print(f"Afiliações: {', '.join(listaAfiliacoes)}")
                    if pub.get('doi'):
                        print(f"DOI: {pub['doi']}")
                    if pub.get('publish_date'):
                        print(f"Data da Publicação: {pub['publish_date']}")
                    print("\n")
            
        else:
            print("Opção inválida! Exibindo autores em ordem aleatória:")
            if publicacoes_encontradas:
                for pub in publicacoes_encontradas:
                    if pub.get('title'):
                        print(f"Título: {pub['title']}\n")
                    if pub.get('abstract'):
                        print(f"Resumo: {pub['abstract']}\n")
                    if pub.get('keywords'):
                        listaKeywords = [palavra.strip(". ") for palavra in pub['keywords'].split(", ")]
                        print(f"Palavras-Chave: {', '.join(listaKeywords)}\n")
                    if pub.get('authors'):
                        listaAutores = []
                        listaAfiliacoes = []
                        for p in pub['authors']:
                            if p.get('name'):
                                nomeAutor = p['name']
                                listaAutores.append(nomeAutor)
                            if p.get('affiliation'):
                                afiliacaoAutor = p['affiliation']
                                if afiliacaoAutor not in listaAfiliacoes:
                                    listaAfiliacoes.append(afiliacaoAutor)
                        print(f"Autores: {', '.join(listaAutores)}\n")
                        print(f"Afiliações: {', '.join(listaAfiliacoes)}\n")
                    if pub.get('doi'):
                        print(f"DOI: {pub['doi']}\n")
                    if pub.get('publish_date'):
                        print(f"Data da Publicação: {pub['publish_date']}")
    
    else:
        print("Nenhuma publicação encontrada com o critério especificado.")

# ----------------------------------------------------------------------
# Função para ATUALIZAR uma publicação existente
def atualizarPublicacao(dados, indice):
    if 0 <= indice < len(dados):
        publicacao = dados[indice]
        print("\n----- Atualizar Publicação -----\n")
        print(f"Se não desejar atualizar o parâmetro, deixe em branco.\n")

        if publicacao.get('title'):
            titulo = input(f"Novo título (atual: {publicacao['title']}): ").strip()
            if not titulo:
                titulo = publicacao['title']
            publicacao['title'] = titulo
        
        if publicacao.get('abstract'):
            resumo = input(f"Novo resumo (atual: {publicacao['abstract']}): ").strip()
            if not resumo:
                resumo = publicacao['abstract']
            publicacao['abstract'] = resumo

        if publicacao.get('keywords'):
            lista_palavras_chave = []
            cond = True
            while cond:
                palavra_chave = input("Palavra-chave (deixe em branco para terminar): ").strip()
                if palavra_chave:
                    lista_palavras_chave.append(palavra_chave)
                else:
                    cond = False
            palavras_chave = ", ".join(lista_palavras_chave)
            publicacao['keywords'] = palavras_chave

        if publicacao.get('authors'):
            for autor in publicacao["authors"]:
                nomeAutor = input(f"Novo nome para o autor '{autor['name']}': ").strip()
                if not nomeAutor:
                    nomeAutor = autor["name"]  
                afiliacaoAutor = input(f"Nova afiliação para o autor '{autor['name']}': ").strip()
                if not afiliacaoAutor:
                    afiliacaoAutor = autor["affiliation"]
                autor["name"] = nomeAutor
                autor["affiliation"] = afiliacaoAutor
        
        if publicacao.get('publish_date'):
            nova_data = input(f"Nova data de publicação (atual: {publicacao['publish_date']}): ").strip()
            partes = nova_data.split("-")
            if len(partes) == 3 and all(p.isdigit() for p in partes):
                ano, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
                if 1 <= mes <= 12 and 1 <= dia <= 31:
                    if mes in [4, 6, 9, 11] and dia > 30:
                        print("Mês especificado tem no máximo 30 dias.\n")
                    elif mes == 2 and (dia > 29 or (dia == 29 and ano % 4 != 0)):
                        print("Data inválida em fevereiro.\n")
                    else:
                        publicacao["publish_date"] = f"{ano:04d}-{mes:02d}-{dia:02d}"
                else:
                    print("Mês ou dia fora do intervalo.\n")
            else:
                print("Formato de data inválido. Use YYYY-MM-DD.\n")

        print("Publicação atualizada com sucesso!\n")
        salvarDados(dados)
    else:
        print("Erro: Índice da publicação inválido!\n")

# ----------------------------------------------------------------------
# Função para ELIMINAR uma publicação
def eliminarPublicacao(indice):
    if 0 <= indice < len(dados):
        dados.pop(indice) # pop --> remover um elemento
        salvarDados(dados)
        print(f"Publicação de índice {indice} eliminada com sucesso!\n")
    else:
        print("Erro: Índice da publicação inválido!\n")

# ----------------------------------------------------------------------
# Função para listar AUTORES e as suas PUBLICAÇÕES
def listarAutores():
    autor_publicacoes = {}
    for p in dados:
        if "authors" in p:
            for autor in p["authors"]:
                if autor.get('name'):
                    nome_autor = autor["name"]
                    if nome_autor not in autor_publicacoes:
                        autor_publicacoes[nome_autor] = []
                        if p.get('title'):
                            (autor_publicacoes[nome_autor]).append(p['title'])
                        else:
                            (autor_publicacoes[nome_autor]).append("Publicação sem Título.")
                    else:
                        if p.get('title'):
                            (autor_publicacoes[nome_autor]).append(p['title'])
                        else:
                            (autor_publicacoes[nome_autor]).append("Publicação sem Título.")
  
    with open("listaAutoresPublicacoes.txt", "w", encoding="utf-8") as f:
        f.write("------ AUTORES E RESPETIVAS PUBLICAÇÕES ------\n")
        for autor, publicacoes in autor_publicacoes.items():
            f.write("\n")
            f.write(f"Autor: {autor}\n")
            f.write(f"Publicações:\n")
            for pub in publicacoes:
                f.write(f"  - {pub}\n")
            f.write("\n")
    
    print("Lista de autores e as suas respetivas publicações gerada com sucesso em 'listaAutoresPublicacoes.txt'.")

# ----------------------------------------------------------------------
# Função para IMPORTAR dados de outro arquivo JSON
def importarDados(ficheiro):
    try:
        with open(ficheiro, encoding='utf-8') as f:
            novos_dados = json.load(f)
            dados.extend(novos_dados)
            salvarDados(dados)
            print(f"Dados importados com sucesso do ficheiro {ficheiro}!\n")
    except Exception as e:
        print(f"Erro ao importar dados: {e}\n")
    
# ----------------------------------------------------------------------
# Função para gerar RELATÓRIOS de ESTATÍSTICAS
import matplotlib.pyplot as plt
import numpy as np

def gerarRelatorios():
    
    print("""
Gerar Relatórios:
(1) Distribuição de Publicações por Ano
(2) Distribuição de Palavras-Chave por Frequência
(3) Distribuição de Publicações Por Autor
(4) Distribuição de Publicações por Mês de um Ano
(5) Distribuição de Publicações de um Autor por Anos
(6) Distribuição de Palavra-Chave Mais Frequente por Ano
(7) Sair - Terminar Relatórios          
""")
    
    with open("relatorio.md", "w", encoding="utf-8") as f: # .md --> markdown --> suporta texto e imagens(gráfico)
        f.write("RELATÓRIO DE ESTATÍSTICAS\n")

    cond = True
    while cond:
        comando = input("Digite um comando para gerar o seu relatório (1-7): ")

        # Distribuição de Publicações por Ano :)
        if comando == "1":
            publicacoes_por_ano = {}
            for p in dados:
                if p.get("publish_date"):
                    ano = p["publish_date"].split("-")[0]
                    if ano not in publicacoes_por_ano:
                        publicacoes_por_ano[ano] = 1
                    else:
                        publicacoes_por_ano[ano] = publicacoes_por_ano[ano] + 1

            # Converte o dicionário "anos_ordenados" numa lista de tuplos (ano, nº de publicações)
            # Ordena os tuplos com base no seu 1º elemento = ano
            anos_ordenados = sorted(publicacoes_por_ano.items(), key=lambda x: x[0])

            ano = [x[0] for x in anos_ordenados]
            contagem_publicacoes = [x[1] for x in anos_ordenados]

            # Gerar Gráfico de Barras Verticais
            plt.bar(ano, contagem_publicacoes, color="tomato")
            plt.xlabel("Anos", weight='bold', labelpad = 10)
            plt.ylabel("Número de Publicações", weight='bold', labelpad = 10)
            plt.title("Distribuição de Publicações por Ano", weight='bold')
            plt.xticks(rotation=45, ha='right')  # Rotaciona os anos em 45 graus e alinha à direita
            plt.tight_layout() # Ajusta automaticamente os elementos do gráfico para evitar sobreposição

            for i in range(len(ano)):
            # Ajusta posição do texto dinamicamente
                posicao_y = contagem_publicacoes[i] + 2
                plt.text(
                    x=ano[i], 
                    y=posicao_y,  # Posição ajustada
                    s=str(contagem_publicacoes[i]),  # Texto a ser exibido
                    ha='center',  # Alinhamento horizontal
                    fontsize=8,
                    color="black"
                )

            # Salvar Gráfico como Imagem
            grafico1 = "publicacoesPorAno.png"
            plt.savefig(grafico1)
            plt.close()

            with open("relatorio.md", "a", encoding="utf-8") as f: # "a" --> add (se escrevesse "w", apagava tudo o que o ficheiro já tinha)
                f.write("\nNúmero de publicações por ano\n")
                for ano, contagem_publicacoes in anos_ordenados:
                    f.write(f"- {ano}: {contagem_publicacoes}\n")
                f.write("\n")
                f.write("Gráfico de Distribuição de Publicações por Ano\n")
                f.write(f"![Gráfico de Distribuição de Publicações por Ano]({grafico1})\n")
        
            print(f"Relatório gerado com sucesso em 'relatorio.md' e gráfico salvo em '{grafico1}'.")

        # Distribuição de Palavras-Chave por Frequência
        elif comando == "2":
            palavras_chave_freq = {}
            for p in dados:
                if p.get("keywords"):
                    listaPalavras = [palavra.strip(". ") for palavra in p['keywords'].split(", ")]
                    for palavra in listaPalavras:
                        palavra = palavra.strip("., ")
                        if palavra not in palavras_chave_freq:
                            palavras_chave_freq[palavra] = 1
                        else:
                            palavras_chave_freq[palavra] = palavras_chave_freq[palavra] + 1

            palavras_ordenadas = sorted(palavras_chave_freq.items(), key=lambda x: x[1], reverse=True)
            top20_palavras = palavras_ordenadas[:20]

            palavra = [x[0] for x in top20_palavras]
            frequencia = [x[1] for x in top20_palavras]

            # Gerar Gráfico de Barras Horizontais
            bars = plt.barh(palavra, frequencia, color="plum")
            for bar in bars:
                if bar.get_width() > 22:  # Se o comprimento da barra > 22, colocar o texto dentro da barra
                    plt.text(bar.get_width() - 5, bar.get_y() + bar.get_height() / 2, str(int(bar.get_width())), va='center', ha='right', color='black', fontsize=9)
                else:  # Caso contrário, colocar o texto fora
                    plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2, str(int(bar.get_width())), va='center', ha='left', color='black', fontsize=9)

            plt.xlabel("Frequência", fontsize=10, weight='bold', labelpad=10)
            plt.ylabel("Palavras-Chave", fontsize=10, weight='bold', labelpad=10)
            plt.title("Top 20 Palavras-Chave por Frequência", fontsize=12, weight='bold')
            plt.gca().invert_yaxis() # Inverte para a + frequente no topo
            plt.tight_layout()

            # Salvar o gráfico como imagem
            grafico2 = "frequenciasPalavrasChave.png"
            plt.savefig(grafico2)
            plt.close()

            with open("relatorio.md", "a", encoding="utf-8") as f:
                f.write("\nFrequência de palavras-chave:\n")
                for palavra, frequencia in top20_palavras:
                    f.write(f"- {palavra}: {frequencia}\n")
                f.write("\n")
                f.write("Gráfico de Distribuição de Palavras-Chave por Frequência - Top 20 Palavras\n")
                f.write(f"![Gráfico de Distribuição de Palavras-Chave por Frequência]({grafico2})\n")
        
            print(f"Relatório gerado com sucesso em 'relatorio.md' e gráfico salvo em '{grafico2}'.")
            
        # Distribuição de Publicações Por Autor (AINDA NAO ESTA DIREITO)
        elif comando == "3":
            publicacoes_por_autor = {}
            for p in dados:
                if p.get("authors"):
                    for autor in p["authors"]:
                        nome_autor = autor["name"]
                        if nome_autor not in publicacoes_por_autor:
                            publicacoes_por_autor[nome_autor] = 1
                        else:
                            publicacoes_por_autor[nome_autor] = publicacoes_por_autor[nome_autor] + 1

            autores_ordenados = sorted(publicacoes_por_autor.items(), key=lambda x: x[1], reverse=True)
            top20_autores = autores_ordenados[:20]
            nomes = [x[0] for x in top20_autores]
            n_publicacoes = [x[1] for x in top20_autores]

            # Gerar Gráfico
            bars = plt.barh(nomes, n_publicacoes, color="pink")
            for bar in bars:
                plt.text(bar.get_width() - 1, bar.get_y() + bar.get_height() / 2, str(int(bar.get_width())), va='center', ha='right', color='black', fontsize=9)
            plt.xlabel("Número de Publicações", fontsize=10, weight='bold', labelpad=10)
            plt.ylabel("Autores", fontsize=10, weight='bold', labelpad=10)
            plt.title("Top 20 Autores por Número de Publicações", fontsize=10, weight='bold')
            plt.gca().invert_yaxis()  # Inverte para o maior no topo
            plt.tight_layout()

            # Salvar o gráfico como imagem
            grafico3 = "publicacoesPorAutor.png"
            plt.savefig(grafico3)
            plt.close()

            with open("relatorio.md", "a", encoding="utf-8") as f:
                f.write("\nNúmero de publicações por autor:\n")
                for nomes, n_publicacoes in top20_autores:
                    f.write(f"- {nomes}: {n_publicacoes}\n")
                f.write("\n")
                f.write("Gráfico de Distribuição de Publicações por Autor - Top 20 Autores\n")
                f.write(f"![Gráfico de Distribuição de Publicações por Autor\n]({grafico3})\n")
        
            print(f"Relatório gerado com sucesso em 'relatorio.md' e gráfico salvo em '{grafico3}'.")

        # Distribuição de Publicações por Mês de um Determinado Ano
        elif comando == "4":
            ano_escolhido = int(input("Ano: "))
            contagem_meses = {mes: 0 for mes in range(1, 13)}
            # dicionário em compreensão --> chave = todos os números de 1-12 (meses) : valores = 0
            # contagem_meses = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0 }

            for p in dados:
                if p.get('publish_date'):
                    partes_data = p['publish_date'].split("-")
                    if all(x.isdigit() for x in partes_data):
                        ano = int(partes_data[0])
                        mes = int(partes_data[1])
                        if ano == ano_escolhido:
                            contagem_meses[mes] = contagem_meses[mes] + 1

            # Gerar Gráfico de Pizza (Pie Chart)
            
            labels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
            sizes = [x[1] for x in contagem_meses.items()]
            sizes_filtrados = [size for size in sizes if size > 0]
            labels_filtrados = [label for size, label in zip(sizes, labels) if size > 0]
            # zip(sizes, labels) combina as 2 listas em pares
            # Quando iteramos em zip, podemos aplicar condições aos pares, garantindo que valores e rótulos correspondam
        
            fig, ax = plt.subplots()
            ax.pie(sizes_filtrados, labels=labels_filtrados, autopct=lambda p: f'{int(p/100.*sum(sizes_filtrados))}', startangle=90, colors = ['lightpink', 'skyblue', 'plum'])
            # autopct=lambda p: f'{int(p/100.*sum(sizes_filtrados))}'
            # - Define uma função sem nome (lambda) que recebe um argumento p (no contexto do ax.pie(), o p é a % calculada automaticamente pelo Matplotlib para cada fatia do gráfico)
            # - Converte X% para 0,0X
            # - Multiplica esse valor (fração de cada elemento) pela soma dos valores em "sizes_filtrados"
            ax.set_title(f"Número de Publicações por Mês em {ano_escolhido}")

            # Salvar Gráfico como Imagem
            grafico4 = f"publicacoesPorMesDe{ano_escolhido}.png"
            plt.savefig(grafico4)
            plt.close()
    
            with open("relatorio.md", "a", encoding="utf-8") as f:
                f.write(f"\nNúmero de Publicações por Mês em {ano_escolhido}:\n")
                for mes, publicacoes in contagem_meses.items():
                    f.write(f"- {mes}: {publicacoes}\n")
                f.write("\n")
                f.write(f"Gráfico de Distribuição de Publicações por Mês em {ano_escolhido} \n")
                f.write(f"![Gráfico de Distribuição de Publicações por Mês em {ano_escolhido}]({grafico4})\n")
        
            print(f"Relatório gerado com sucesso em 'relatorio.md' e gráfico salvo em '{grafico4}'.")

        # Distribuição de Publicações de um Autor por Anos
        elif comando == "5":
            autor_escolhido = input("Autor: ")
            contagem_anos = {}
            for p in dados:
                if p.get('authors') and p.get('publish_date'):
                    ano = int(p["publish_date"].split("-")[0])
                    for autor in p["authors"]:
                        if autor.get("name").lower() == autor_escolhido.lower():
                            if ano not in contagem_anos:
                                contagem_anos[ano] = 1
                            else:
                                contagem_anos[ano] = contagem_anos[ano] + 1

            anos_ordenados = sorted(contagem_anos.items(), key=lambda x: x[0])
            anos = [x[0] for x in anos_ordenados]
            quantidades = [x[1] for x in anos_ordenados]

            # Gerar Gráfico de Pizza (Pie Chart)
            
            labels = anos
            sizes = quantidades
            
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct=lambda p: f'{int(p/100.*sum(sizes))}', startangle=90, colors = ['lightskyblue', 'lightgreen', 'khaki'])
            ax.set_title(f"Número de Publicações de {autor_escolhido} por Anos")

            # Salvar o gráfico como imagem
            grafico5 = f"publicacoesPorAnosDe{autor_escolhido}.png"
            plt.savefig(grafico5)
            plt.close()

            # Escrever Relatório
            with open("relatorio.md", "a", encoding="utf-8") as f:
                f.write(f"\nNúmero de Publicações por Anos de {autor_escolhido}:\n")
                for anos, quantidades in anos_ordenados:
                    f.write(f"- {anos}: {quantidades}\n")
                f.write("\n")
                f.write(f"Gráfico de Distribuição de Publicações por Anos de {autor_escolhido}\n")
                f.write(f"![Gráfico de Distribuição de Publicações por Anos de {autor_escolhido}]({grafico5})\n")
        
            print(f"Relatório gerado com sucesso em 'relatorio.md' e gráfico salvo em '{grafico5}'.")
    

        # Distribuição de Palavra-Chave Mais Frequente por Ano:
        elif comando == "6":
            palavras_chave_ano = {}
            for p in dados:
                if p.get('keywords') and p.get('publish_date'):
                    ano = int(p["publish_date"].split("-")[0])
                    lista_palavras = [palavra.strip(". ") for palavra in p['keywords'].split(", ")]

                    if ano not in palavras_chave_ano:
                        palavras_chave_ano[ano] = {}
                
                    for palavra in lista_palavras:
                        if palavra not in palavras_chave_ano[ano]:
                            palavras_chave_ano[ano][palavra] = 1
                        else:
                            palavras_chave_ano[ano][palavra] = palavras_chave_ano[ano][palavra] + 1
                
            # Encontrar a palavra-chave + frequente por ano
            palavras_frequentes_por_ano = {}
            for ano, palavras in palavras_chave_ano.items():
                palavra_mais_frequente = max(palavras.items(), key=lambda x: x[1])  # Escolhe a palavra com + frequência
                palavras_frequentes_por_ano[ano] = palavra_mais_frequente

            # Ordenar os anos
            anos_ordenados = sorted(palavras_frequentes_por_ano.items(), key=lambda x: x[0], reverse=True)
            anos = [x[0] for x in anos_ordenados]
            palavras = [x[1][0] for x in anos_ordenados]
            frequencias = [x[1][1] for x in anos_ordenados]

            # Gerar Gráfico de Linhas com Marcadores
            plt.figure(figsize=(10, 6))
            plt.plot(anos, frequencias, marker='o', color="maroon", linestyle='-', linewidth=2, markersize=6)

            labels = [f"{ano}: {palavra}" for ano, palavra in zip(anos, palavras)]
            handles = [plt.Line2D([0], [0], color='maroon', marker='o', linestyle='-', markersize=6, label=label) for label in labels]
            plt.legend(handles=handles, ncol=3, loc="lower left", fontsize=10, title="Palavra Mais Frequente por Ano")

            # Configurar títulos e rótulos
            plt.xlabel("Anos", fontsize=12, weight='bold', labelpad=12)
            plt.ylabel("Frequência da Palavra-Chave", fontsize=12, weight='bold', labelpad=12)
            plt.title("Palavra-Chave Mais Frequente por Ano", fontsize=14, weight='bold')
            plt.xticks(anos, rotation=45)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()

            # Salvar o gráfico como imagem
            grafico6 = "palavraMaisFrequentePorAno.png"
            plt.savefig(grafico6)
            plt.close()

            # Escrever o relatório
            with open("relatorio.md", "a", encoding="utf-8") as f:
                f.write("\nPalavra-chave mais frequente por ano:\n")
                for ano, (palavra, frequencia) in palavras_frequentes_por_ano.items():
                    f.write(f"- {ano}: {palavra} ({frequencia} ocorrências)\n")
                f.write("\n")
                f.write("Gráfico de Palavra-Chave Mais Frequente por Ano\n")
                f.write(f"![Gráfico de Palavra-Chave Mais Frequente por Ano]({grafico6})\n")
        
            print(f"Relatório gerado com sucesso em 'relatorio.md' e gráfico salvo em '{grafico6}'.")
    
        elif comando == "7":
            cond = False
            print("Relatórios de estatísticas terminados.")
        else:
            print("Comando inválido! Insira um número entre 1 e 7. \n")


# REQUISITOS DO SISTEMA

# ----------------------------------------------------------------------
# Função para análise de PUBLICAÇÕES por AUTOR
def analisePorAutor():
    dicionario_autores = {}

    for p in dados:
        if p.get('authors'):
            for autor in p["authors"]:
                if autor.get('name'):
                    nome_autor = autor["name"]
                    if nome_autor not in dicionario_autores:
                        dicionario_autores[nome_autor] = []
                        dicionario_autores[nome_autor].append(p)
                    else:
                        dicionario_autores[nome_autor].append(p)
                        

    print("\n------------- ANÁLISE DE PUBLICAÇÕES POR AUTOR -------------")
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

    with open("analisePublicacoesAutores.txt", "w", encoding="utf-8") as f:
        f.write("------ AUTORES E ARTIGOS PUBLICADOS ------\n")
        for autor, artigos in autores_ordenados:
            f.write(f"\nAutor: {autor} ({len(artigos)} artigos publicados)\n")
            for i, p in enumerate(artigos, start=1):
                if p.get('title'):
                    if p.get('publish_date'):
                        f.write(f"({i}) {p['title']} (Publicado em {p['publish_date']})\n")
                    else:
                        f.write(f"({i}) {p['title']} (Publicação sem data referida)\n")
                else:
                    f.write(f"({i}) Publicação sem título.\n")
            f.write("\n")
    
    print(f"Análise de publicações por autor gerada com sucesso em 'analisePublicacoesAutores'.")

# ----------------------------------------------------------------------
# Função para análise de PUBLICAÇÕES por PALAVRA-CHAVE
def analisePorPalavraChave():
    dicionario_palavras = {}

    for p in dados:
        if p.get('keywords'):
            listaKeywords = [palavra.strip(". ") for palavra in p['keywords'].split(", ")]
            for palavra in listaKeywords:
                if palavra not in dicionario_palavras:
                    dicionario_palavras[palavra] = []
                    dicionario_palavras[palavra].append(p)
                else:
                    dicionario_palavras[palavra].append(p)

    print("------------- ANÁLISE DE PUBLICAÇÕES POR PALAVRA-CHAVE -------------")
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

    with open("analisePublicacoesPalavrasChave.txt", "w", encoding="utf-8") as f:
        f.write("------ PALAVRAS-CHAVE E ARTIGOS PUBLICADOS ------\n")
        for palavra, artigos in palavras_ordenadas:
            f.write(f"\nPalavra-chave: '{palavra}' ({len(artigos)} ocorrências)\n")
            for i, p in enumerate(artigos, start=1):
                if p.get('title'):
                    if p.get('publish_date'):
                        f.write(f"({i}) {p['title']} (Publicado em {p['publish_date']})\n")
                    else:
                        f.write(f"({i}) {p['title']} (Publicação sem data referida)\n")
                else:
                    f.write(f"({i}) Publicação sem título.\n")
            f.write("\n")
    
    print(f"Análise de publicações por palavra-chave gerada com sucesso em 'analisePublicacoesPalavrasChave'.")

# ----------------------------------------------------------------------
# Função para exibir a mensagem de ajuda
def exibirAjuda():
    print("""
Comandos disponíveis:
(1) Criar Publicação - Criar uma nova publicação
(2) Consultar Publicação - Consultar uma publicação através do seu índice
(3) Filtrar Publicações - Listar publicações que obedeçam a filtros
(4) Atualizar Publicação - Atualizar uma publicação existente
(5) Eliminar Publicação - Eliminar uma publicação existente
(6) Listar Autores - Listar todos os autores e as suas publicações
(7) Importar Publicações - Importar publicações de um arquivo JSON
(8) Relatório de Estatísticas - Gerar relatórios de estatísticas
(9) Analisar Publicações por Autor - Listar publicações que contenham um determinado autor
(10) Analisar Publicações por Palavra-Chave - Listar publicações que contenham uma certa palavra-chave
(11) Help - Exibir esta mensagem de ajuda
(12) Sair - Sair do programa
""")

# ----------------------------------------------------------------------
# Função principal para o menu de linha de comando
def menu():
    cond = True
    while cond:
        comando = input("Digite um comando (ou 'Help' para ver os comandos disponíveis): ").strip().lower()
        if comando == "criar publicação" or comando == "1":
            criarPublicacao()
        elif comando == "consulta de publicação" or comando == "2":
            indice = int(input("Digite o índice da publicação: ").strip())
            consultarPublicacao(indice)
        elif comando == "consultar publicações" or comando == "3":
            consultarPublicacoes()
        elif comando == "atualizar publicação" or comando == "4":
            indice = int(input("Digite o índice da publicação: ").strip())
            atualizarPublicacao(dados, indice)
        elif comando == "eliminar publicação" or comando == "5":
            indice = int(input("Digite o índice da publicação: ").strip())
            eliminarPublicacao(indice)
        elif comando == "listar autores" or comando == "6":
            listarAutores()
        elif comando == "importar publicações" or comando == "7":
            ficheiro = input("Digite o caminho do arquivo JSON: ").strip()
            importarDados(ficheiro)
        elif comando == "relatório de estatísticas" or comando == "8":
            gerarRelatorios()
        elif comando == "analisar publicações por autor" or comando == "9":
            analisePorAutor()
        elif comando == "analisar publicações por palavra-chave" or comando == "10":
            analisePorPalavraChave()
        elif comando == "help" or comando == "11":
            exibirAjuda()
        elif comando == "sair" or comando == "12":
            cond = False
            print("Até à próxima...")
        else:
            print("Comando inválido! Digite 'Help' para ver os comandos disponíveis.\n")

# Executar o menu de linha de comando
if __name__ == "__main__":
    menu()

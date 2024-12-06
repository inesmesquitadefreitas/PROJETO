import json

# Carregar dados do arquivo JSON
def carregaDADOS(fnome):
    with open(fnome, encoding='utf-8') as f:
        return json.load(f)

# Salvar dados no arquivo JSON
def salvarDados(dados, ficheiro="Dados_Projeto.json"):
    with open(ficheiro, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)
    with open("output.txt", "a", encoding="utf-8") as f:
        f.write(f"Dados salvos com sucesso no ficheiro {ficheiro}!\n")

# Carregar dados no início do programa
dados = carregaDADOS("/home/heitor/Documents/PROJETO/Dados_Projeto.json")

# Função para criar uma nova publicação
def criarPublicacao():
    with open("output.txt", "a", encoding="utf-8") as f:
        f.write(" -------- NOVA PUBLICAÇÃO --------\n")
    titulo = input("Título do artigo: ").strip()
    resumo = input("Resumo do artigo: ").strip()
    palavras_chave = input("Palavras-chave (separadas por vírgula): ").strip().split(",")
    doi = input("DOI: ").strip()
    url_pdf = input("URL do PDF: ").strip()
    url_artigo = input("URL do artigo: ").strip()

    autores = []
    while True:
        nome_autor = input("Nome do autor (deixe em branco para terminar): ").strip()
        if not nome_autor:
            break
        autor_afiliacao = input(f"Afiliação do autor {nome_autor}: ").strip()
        autores.append({"Nome": nome_autor, "Afiliação": autor_afiliacao})

    data_publicacao = ""
    while not data_publicacao:
        data_input = input("Data de Publicação (YYYY-MM-DD): ").strip()
        partes_data = data_input.split("-")
        if len(partes_data) == 3 and all(p.isdigit() for p in partes_data):
            ano, mes, dia = int(partes_data[0]), int(partes_data[1]), int(partes_data[2])
            if 1 <= mes <= 12 and 1 <= dia <= 31:
                if mes in [4, 6, 9, 11] and dia > 30:
                    with open("output.txt", "a", encoding="utf-8") as f:
                        f.write("Mês especificado tem no máximo 30 dias.\n")
                elif mes == 2 and (dia > 29 or (dia == 29 and ano % 4 != 0)):
                    with open("output.txt", "a", encoding="utf-8") as f:
                        f.write("Data inválida em fevereiro.\n")
                else:
                    data_publicacao = f"{ano:04d}-{mes:02d}-{dia:02d}"
            else:
                with open("output.txt", "a", encoding="utf-8") as f:
                    f.write("Mês ou dia fora do intervalo.\n")
        else:
            with open("output.txt", "a", encoding="utf-8") as f:
                f.write("Formato de data inválido. Use YYYY-MM-DD.\n")

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

    dados.append(nova_publicacao)
    salvarDados(dados)

# Função para atualizar uma publicação existente
def atualizarPublicacao(publicacoes, indice):
    if 0 <= indice < len(publicacoes):
        publicacao = publicacoes[indice]
        with open("output.txt", "a", encoding="utf-8") as f:
            f.write(f"Atualizando a publicação: {publicacao['Título']}\n")

        titulo = input(f"Novo título (atual: {publicacao['Título']}): ").strip() or publicacao['Título']
        resumo = input(f"Novo resumo (atual: {publicacao['Resumo']}): ").strip() or publicacao['Resumo']
        palavras_chave = input(f"Novas palavras-chave (atual: {publicacao['Palavras-Chave']}): ").strip() or publicacao['Palavras-Chave']
        publicacao['Título'] = titulo
        publicacao['Resumo'] = resumo
        publicacao['Palavras-Chave'] = [palavra.strip() for palavra in palavras_chave.split(",")]

        for autor in publicacao["Autores"]:
            autor["Nome"] = input(f"Novo nome para o autor '{autor['Nome']}' (deixe em branco para não alterar): ").strip() or autor["Nome"]
            autor["Afiliação"] = input(f"Nova afiliação para o autor '{autor['Nome']}' (deixe em branco para não alterar): ").strip() or autor["Afiliação"]

        nova_data = input(f"Nova data de publicação (atual: {publicacao['Data da Publicação']}): ").strip()
        partes = nova_data.split("-")
        if len(partes) == 3 and all(p.isdigit() for p in partes):
            ano, mes, dia = int(partes[0]), int(partes[1]), int(partes[2])
            if 1 <= mes <= 12 and 1 <= dia <= 31:
                if mes in [4, 6, 9, 11] and dia > 30:
                    with open("output.txt", "a", encoding="utf-8") as f:
                        f.write("Mês especificado tem no máximo 30 dias.\n")
                elif mes == 2 and (dia > 29 or (dia == 29 and ano % 4 != 0)):
                    with open("output.txt", "a", encoding="utf-8") as f:
                        f.write("Data inválida em fevereiro.\n")
                else:
                    publicacao["Data da Publicação"] = f"{ano:04d}-{mes:02d}-{dia:02d}"
            else:
                with open("output.txt", "a", encoding="utf-8") as f:
                    f.write("Mês ou dia fora do intervalo.\n")
        else:
            with open("output.txt", "a", encoding="utf-8") as f:
                f.write("Formato de data inválido. Use YYYY-MM-DD.\n")

        with open("output.txt", "a", encoding="utf-8") as f:
            f.write("Publicação atualizada com sucesso!\n")
        salvarDados(publicacoes)
    else:
        with open("output.txt", "a", encoding="utf-8") as f:
            f.write("Erro: Índice da publicação inválido!\n")

# Função para importar dados de outro arquivo JSON
def importarDados(ficheiro):
    try:
        with open(ficheiro, encoding='utf-8') as f:
            novos_dados = json.load(f)
            dados.extend(novos_dados)
            salvarDados(dados)
            with open("output.txt", "a", encoding="utf-8") as f:
                f.write(f"Dados importados com sucesso do ficheiro {ficheiro}!\n")
    except Exception as e:
        with open("output.txt", "a", encoding="utf-8") as f:
            f.write(f"Erro ao importar dados: {e}\n")

# Função para consultar uma publicação específica
def consultarPublicacao(indice):
    if 0 <= indice < len(dados):
        publicacao = dados[indice]
        with open("output.txt", "a", encoding="utf-8") as f:
            f.write(f"--- Publicação {indice} ---\n")
            f.write(f"Título: {publicacao['Título']}\n")
            f.write(f"Resumo: {publicacao['Resumo']}\n")
            f.write(f"Palavras-Chave: {', '.join(publicacao['Palavras-Chave'])}\n")
            f.write(f"DOI: {publicacao['DOI']}\n")
            f.write(f"URL do PDF: {publicacao['URL do PDF']}\n")
            f.write(f"Data da Publicação: {publicacao['Data da Publicação']}\n")
            f.write(f"URL do Artigo: {publicacao['URL do Artigo']}\n")
            f.write(f"Autores: {', '.join(autor['Nome'] for autor in publicacao['Autores'])}\n")
    else:
        with open("output.txt", "a", encoding="utf-8") as f:
            f.write("Erro: Índice da publicação inválido!\n")

# Função para consultar publicações com filtros
def consultarPublicacoes():
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
        with open("output.txt", "a", encoding="utf-8") as f:
            f.write("Opção inválida!\n")
        return

    publicacoes_encontradas = []
    for p in dados:
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
    
    publicacoes_encontradas.sort(key=lambda x: (x["Data da Publicação"], x["Título"].lower()))
    
    with open("output.txt", "a", encoding="utf-8") as f:
        if publicacoes_encontradas:
            f.write("--- RESULTADOS DA PESQUISA ---\n")
            for i, p in enumerate(publicacoes_encontradas, start=1):
                f.write(f"{i}) Título: {p['Título']}\n")
                f.write(f"   Data da Publicação: {p['Data da Publicação']}\n")
                f.write(f"   Autores: {', '.join(autor['Nome'] for autor in p['Autores'])}\n")
                f.write(f"   DOI: {p['DOI']}\n")
                f.write(f"   Palavras-Chave: {', '.join(p['Palavras-Chave'])}\n")
        else:
            f.write("Nenhuma publicação encontrada com o critério especificado.\n")

# Função para eliminar uma publicação
def eliminarPublicacao(indice):
    if 0 <= indice < len(dados):
        dados.pop(indice)
        salvarDados(dados)
        with open("output.txt", "a", encoding="utf-8") as f:
            f.write(f"Publicação {indice} eliminada com sucesso!\n")
    else:
        with open("output.txt", "a", encoding="utf-8") as f:
            f.write("Erro: Índice da publicação inválido!\n")

# Função para listar autores e suas publicações
def listarAutores():
    autores = {}
    for p in dados:
        if "Autores" in p:
            for autor in p["Autores"]:
                nome_autor = autor["Nome"]
                if nome_autor not in autores:
                    autores[nome_autor] = []
                autores[nome_autor].append(p["Título"])
        else:
            with open("output.txt", "a", encoding="utf-8") as f:
                f.write(f"Publicação sem autores encontrada: {p}\n")

    with open("output.txt", "a", encoding="utf-8") as f:
        f.write("--- LISTA DE AUTORES ---\n")
        for autor, publicacoes in autores.items():
            f.write(f"Autor: {autor}\n")
            for pub in publicacoes:
                f.write(f"  - {pub}\n")

# Função para gerar relatórios de estatísticas
def gerarRelatorios():
    palavras_chave = {}
    publicacoes_por_autor = {}
    publicacoes_por_ano = {}

    for p in dados:
        ano = p["Data da Publicação"].split("-")[0]
        if ano not in publicacoes_por_ano:
            publicacoes_por_ano[ano] = 0
        publicacoes_por_ano[ano] += 1

        for palavra in p["Palavras-Chave"]:
            if palavra not in palavras_chave:
                palavras_chave[palavra] = 0
            palavras_chave[palavra] += 1

        for autor in p["Autores"]:
            nome_autor = autor["Nome"]
            if nome_autor not in publicacoes_por_autor:
                publicacoes_por_autor[nome_autor] = 0
            publicacoes_por_autor[nome_autor] += 1

    with open("output.txt", "a", encoding="utf-8") as f:
        f.write("--- RELATÓRIO DE ESTATÍSTICAS ---\n")
        f.write("Número de publicações por ano:\n")
        for ano, count in publicacoes_por_ano.items():
            f.write(f"{ano}: {count}\n")

        f.write("\nNúmero de publicações por autor:\n")
        for autor, count in publicacoes_por_autor.items():
            f.write(f"{autor}: {count}\n")

        f.write("\nFrequência de palavras-chave:\n")
        for palavra, count in palavras_chave.items():
            f.write(f"{palavra}: {count}\n")

# Função para exibir a mensagem de ajuda
def exibirAjuda():
    with open("output.txt", "a", encoding="utf-8") as f:
        f.write("""
Comandos disponíveis:
1. Criar Publicação - Criar uma nova publicação
2. Consulta de Publicação - Consultar uma publicação específica
3. Consultar Publicações - Listar todas as publicações com filtros
4. Atualizar Publicação - Atualizar uma publicação existente
5. Eliminar Publicação - Eliminar uma publicação
6. Listar Autores - Listar todos os autores e suas publicações
7. Importar Publicações - Importar publicações de um arquivo JSON
8. Relatório de Estatísticas - Gerar relatórios de estatísticas
9. Help - Exibir esta mensagem de ajuda
10. Sair - Sair do programa
""")

# Função principal para o menu de linha de comando
def menu():
    while True:
        comando = input("Digite um comando (ou 'Help' para ver os comandos disponíveis): ").strip().lower()
        if comando == "criar publicação":
            criarPublicacao()
        elif comando == "consulta de publicação":
            indice = int(input("Digite o índice da publicação: ").strip())
            consultarPublicacao(indice)
        elif comando == "consultar publicações":
            consultarPublicacoes()
        elif comando == "atualizar publicação":
            indice = int(input("Digite o índice da publicação: ").strip())
            atualizarPublicacao(dados, indice)
        elif comando == "eliminar publicação":
            indice = int(input("Digite o índice da publicação: ").strip())
            eliminarPublicacao(indice)
        elif comando == "listar autores":
            listarAutores()
        elif comando == "importar publicações":
            ficheiro = input("Digite o caminho do arquivo JSON: ").strip()
            importarDados(ficheiro)
        elif comando == "relatório de estatísticas":
            gerarRelatorios()
        elif comando == "help":
            exibirAjuda()
        elif comando == "sair":
            break
        else:
            with open("output.txt", "a", encoding="utf-8") as f:
                f.write("Comando inválido! Digite 'Help' para ver os comandos disponíveis.\n")

# Executar o menu de linha de comando
if __name__ == "__main__":
    menu()

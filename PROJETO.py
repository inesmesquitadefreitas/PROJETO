import json
import FreeSimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------
# Carregar dados do arquivo JSON ✔
def carregaDADOS(fnome):
    with open(fnome, encoding='utf-8') as f:
        return json.load(f)

# Salvar dados no arquivo JSON
def salvarDados(dados, ficheiro="ataMedicaPapers.json"):
    try:
        with open(ficheiro, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
            sg.popup(f"Dados salvos com sucesso no ficheiro {ficheiro}!")
    except Exception as e:
        sg.popup_error(f"Erro ao salvar dados no ficheiro {ficheiro}: {e}")

# Carregar dados no início do programa
dados = carregaDADOS("C:/Users/Inês Mesquita/Documents/Eng_Biomédica/Programação/Projeto/ataMedicaPapers.json")
# ----------------------------------------------------------------------
# Função para CRIAR uma nova publicação ✔
def criarPublicacao():
    layout = [
        [sg.Text("Título:"), sg.InputText(key="titulo")],
        [sg.Text("Resumo:"), sg.Multiline(key="resumo")],
        [sg.Text("Palavras-chave (separadas por vírgulas):"), sg.InputText(key="palavras_chave")],
        [sg.Text("DOI:"), sg.InputText(key="doi")],
        [sg.Text("URL do PDF:"), sg.InputText(key="url_pdf")],
        [sg.Text("URL do Artigo:"), sg.InputText(key="url_artigo")],
        [sg.Text("Data de Publicação (YYYY-MM-DD):"), sg.InputText(key="data_publicacao")],
        [sg.Text("Autores e Afiliações:")],
        [sg.Button("Adicionar Autor"), sg.Button("Remover Autor")],
        [sg.Listbox(values=[], size=(40, 5), key="autores", enable_events=True)],
        [sg.Button("Salvar"), sg.Button("Cancelar")],
    ]
    janela = sg.Window("Criar Publicação", layout)

    autores = []
    cond = True
    while cond:
        event, values = janela.read()
        if event in (sg.WINDOW_CLOSED, "Cancelar"):
            cond = False
        elif event == "Adicionar Autor":
            nome_autor = sg.popup_get_text("Nome do Autor:")
            afiliacao = sg.popup_get_text(f"Afiliação de {nome_autor}:")
            if nome_autor and afiliacao:
                autores.append({"name": nome_autor, "affiliation": afiliacao})
                janela["autores"].update([f"{a['name']} ({a['affiliation']})" for a in autores])
        elif event == "Remover Autor":
            selecionado = values["autores"]
            if selecionado:
                autores = [a for a in autores if f"{a['name']} ({a['affiliation']})" not in selecionado]
                janela["autores"].update([f"{a['name']} ({a['affiliation']})" for a in autores])
        elif event == "Salvar":
            nova_publicacao = {
                "title": values["titulo"],
                "abstract": values["resumo"],
                "keywords": values["palavras_chave"],
                "doi": values["doi"],
                "authors": autores,
                "pdf": values["url_pdf"],
                "url": values["url_artigo"],
                "publish_date": values["data_publicacao"],
            }
            dados.append(nova_publicacao)
            salvarDados(dados)
            sg.popup("Publicação criada com sucesso!")
            cond = False

    janela.close()

# ----------------------------------------------------------------------
# Função para CONSULTAR uma publicação específica ✔
def consultarPublicacao():
    sg.theme('LightGrey1')
    layout = [
        [sg.Text("Digite o índice da publicação:"), sg.InputText(key="indice")],
        [sg.Button("Consultar", button_color = ('black', 'pink')), sg.Button("Cancelar", button_color = ('black', 'pink'))],
        [sg.Multiline(size=(60, 15), key="resultado", disabled=True)],
    ]
    janela = sg.Window("Consultar Publicação", layout)

    cond = True
    while cond:
        event, values = janela.read()
        if event in (sg.WINDOW_CLOSED, "Cancelar"):
            cond = False
        elif event == "Consultar":
            try:
                indice = int(values["indice"])
                if 0 <= indice < len(dados):
                    publicacao = dados[indice]
                    resultado = "\n\n".join(
                        [
                            f"Título: {publicacao.get('title', 'N/A')}", # N/A --> Non Available
                            f"Resumo: {publicacao.get('abstract', 'N/A')}",
                            f"Palavras-Chave: {publicacao.get('keywords', 'N/A')}",
                            f"DOI: {publicacao.get('doi', 'N/A')}",
                            f"Autores: {', '.join([a['name'] for a in publicacao.get('authors', [])])}",
                            f"Data de Publicação: {publicacao.get('publish_date', 'N/A')}",
                        ]
                    )
                    janela["resultado"].update(resultado)
                else:
                    sg.popup_error("Índice inválido!")
            except ValueError:
                sg.popup_error("Por favor, insira um número válido.")

    janela.close()

# ----------------------------------------------------------------------
# Função para FILTRAR publicações ✔
def filtrarPublicacoes():
    sg.theme("LightBlue2")
    layout = [
        [sg.Text("Escolha o tipo de filtro:", text_color='crimson')],
        [sg.Button("Título", button_color=("black", "pink")), sg.Button("Autor", button_color=("black", "pink")), sg.Button("Afiliação", button_color=("black", "pink")),
         sg.Button("Data da Publicação", button_color=("black", "pink")), sg.Button("Palavra-Chave", button_color=("black", "pink")), sg.Button("Cancelar", button_color=("black", "pink"))],
        [sg.Multiline(size=(60, 15), key="resultado", disabled=True)],
    ]
    janela = sg.Window("Filtrar Publicações", layout)

    cond = True
    while cond:
        event, values = janela.read()
        if event in (sg.WINDOW_CLOSED, "Cancelar"):
            cond = False
        elif event in ["Título", "Autor", "Afiliação", "Data da Publicação", "Palavra-Chave"]:
            if event in ["Título", "Autor"]:
                filtro = sg.popup_get_text(f"Digite o {event}:")
            elif event in ["Afiliação", "Data da Publicação", "Palavra-Chave"]:
                filtro = sg.popup_get_text(f"Digite a {event}:")
            if filtro:
                chave_filtro = event
                publicacoes_encontradas = []
                for p in dados:
                    if chave_filtro == "Título" and p.get("title") and filtro.lower() in p["title"].lower():
                        publicacoes_encontradas.append(p)
                    elif chave_filtro == "Autor":
                        for autor in p.get("authors", []):
                            if autor.get("name") and filtro.lower() in autor["name"].lower():
                                publicacoes_encontradas.append(p)
                    elif chave_filtro == "Afiliação":
                        for autor in p.get("authors", []):
                            if autor.get("affiliation") and filtro.lower() in autor["affiliation"].lower():
                                publicacoes_encontradas.append(p)
                    elif chave_filtro == "Data da Publicação" and p.get("publish_date") == filtro:
                        publicacoes_encontradas.append(p)
                    elif chave_filtro == "Palavra-Chave" and p.get("keywords"):
                        for k in p["keywords"].split(","):
                            k = k.strip(". ")
                            if filtro.lower() in k.lower():
                                publicacoes_encontradas.append(p)

                if publicacoes_encontradas:
                    resultado = "\n\n".join([
                        f"Título: {p.get('title', 'N/A')}\nAutores: {', '.join([a['name'] for a in p.get('authors', [])])}\nData: {p.get('publish_date', 'N/A')}" for p in publicacoes_encontradas
                    ])
                    janela["resultado"].update(resultado)
                else:
                    sg.popup("Nenhuma publicação encontrada.")

    janela.close()

# ----------------------------------------------------------------------
# Função para ATUALIZAR uma publicação existente ✔
def atualizarPublicacao():
    layout_consulta = [
        [sg.Text("Índice da publicação a atualizar:"), sg.InputText(key="indice")],
        [sg.Button("Atualizar", button_color=("black", "pink")), sg.Button("Cancelar", button_color=("black", "pink"))],
    ]

    janela_consulta = sg.Window("Consultar Publicação", layout_consulta)

    continuar_consulta = True
    while continuar_consulta:
        event, values = janela_consulta.read()

        if event in (sg.WINDOW_CLOSED, "Cancelar"): # sg.WINDOW_CLOSED --> utilizador clicar no X (canto superior direito)
            continuar_consulta = False
            janela_consulta.close()

        elif event == "Atualizar":
            try:
                indice = int(values["indice"])
                if 0 <= indice < len(dados):
                    publicacao = dados[indice]

                    janela_consulta.close() # Fechar a janela de consulta antes de abrir a próxima
                    continuar_consulta = False

                    layout_atualizar = [
                        [sg.Text("Título:"), sg.InputText(publicacao.get("title", ""), key="titulo")],
                        [sg.Text("Resumo:"), sg.Multiline(publicacao.get("abstract", ""), key="resumo")],
                        [sg.Text("Palavras-chave (separadas por vírgulas):"), sg.InputText(publicacao.get("keywords", ""), key="palavras_chave")],
                        [sg.Text("Data de Publicação (YYYY-MM-DD):"), sg.InputText(publicacao.get("publish_date", ""), key="data_publicacao")],
                        [sg.Button("Salvar", button_color=("black", "green")), sg.Button("Cancelar", button_color=("black", "pink"))],
                    ]

                    janela_atualizar = sg.Window("Atualizar Publicação", layout_atualizar)

                    continuar_atualizar = True
                    while continuar_atualizar:
                        event_atualizar, values_atualizar = janela_atualizar.read()

                        if event_atualizar in (sg.WINDOW_CLOSED, "Cancelar"):
                            continuar_atualizar = False
                            janela_atualizar.close()

                        elif event_atualizar == "Salvar":
                            publicacao["title"] = values_atualizar["titulo"]
                            publicacao["abstract"] = values_atualizar["resumo"]
                            publicacao["keywords"] = values_atualizar["palavras_chave"]
                            publicacao["publish_date"] = values_atualizar["data_publicacao"]

                            salvarDados(dados)
                            sg.popup("Publicação atualizada com sucesso!")
                            continuar_atualizar = False
                            janela_atualizar.close()
                else:
                    sg.popup_error("Índice inválido!")
            except ValueError:
                sg.popup_error("Por favor, insira um número válido.")


# ----------------------------------------------------------------------
# Função para ELIMINAR uma publicação ✔
def eliminarPublicacao():
    layout = [
        [sg.Text("Índice da publicação a eliminar:"), sg.InputText(key="indice")],
        [sg.Button("Eliminar", button_color=("white", "red")), sg.Button("Cancelar", button_color=("black", "pink"))],
    ]

    janela = sg.Window("Eliminar Publicação", layout)

    continuar = True
    while continuar:
        event, values = janela.read()

        if event in (sg.WINDOW_CLOSED, "Cancelar"):
            continuar = False
            janela.close()

        elif event == "Eliminar":
            try:
                indice = int(values["indice"])
                if 0 <= indice < len(dados):
                    dados.pop(indice)  # .pop() --> função para remover 1 elemento de uma base de dados
                    salvarDados(dados)
                    sg.popup(f"Publicação de índice {indice} eliminada com sucesso!")
                    continuar = False
                    janela.close()
                else:
                    sg.popup_error("Erro: Índice da publicação inválido!")
            except ValueError:
                sg.popup_error("Por favor, insira um número válido para o índice!")

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
# Função principal para o menu de linha de comando

# Menu Principal
def menu_principal():
    sg.theme("LightGrey1")
    layout = [
        [sg.Text("MENU PRINCIPAL", text_color='crimson', font=("Arial", 16, "bold"))],
        [sg.Button("Criar Publicação", button_color=("black", "pink")),
         sg.Button("Consultar Publicação", button_color=("black", "pink")),
         sg.Button("Filtrar Publicações", button_color=("black", "pink"))],
        [sg.Button("Atualizar Publicação", button_color=("black", "pink")),
         sg.Button("Eliminar Publicação", button_color=("black", "pink")),
         sg.Button("Listar Autores e suas Publicações", button_color=("black", "pink"))],
        [sg.Button("Importar Publicações", button_color=("black", "pink")),
         sg.Button("Gerar Relatórios", button_color=("black", "pink"))],
        [sg.Button("Analisar Publicações por Autor", button_color=("black", "pink")),
         sg.Button("Analisar Publicações por Palavra-Chave", button_color=("black", "pink")),
         sg.Button("Help", button_color=("black", "pink"))],
        [sg.Button("Sair", button_color=("black", "pink"))],
    ]
    return sg.Window("Menu Principal", layout, finalize=True)

# Função Principal da GUI
def gui():
    janela = menu_principal()
    cond = True
    while cond:
        event, _ = janela.read()
        if event in (sg.WINDOW_CLOSED, "Sair"):
            cond = False
        elif event == "Criar Publicação":
            criarPublicacao()
        elif event == "Consultar Publicação":
            consultarPublicacao()
        elif event == "Filtrar Publicações":
            filtrarPublicacoes()
        elif event == "Atualizar Publicação":
            atualizarPublicacao()
        elif event == "Eliminar Publicação":
            eliminarPublicacao()
        elif event == "Listar Autores e suas Publicações":
            listarAutores()
        elif event == "Importar Publicações":
            sg.popup("Função 'Importar Publicações' ainda não implementada.")
        elif event == "Gerar Relatórios":
            gerarRelatorios()
        elif event == "Analisar Publicações por Autor":
            analisePorAutor()
        elif event == "Analisar Publicações por Palavra-Chave":
            analisePorPalavraChave()
        elif event == "Help":
            exibirHelp()
    janela.close()

# Função para Exibir Help
def exibirHelp():
    comandos = """
    COMANDOS DISPONÍVEIS:
    - Criar Publicação: Criar uma nova publicação
    - Consultar Publicação: Consultar uma publicação através do seu índice
    - Filtrar Publicações: Listar publicações que obedeçam a filtros
    - Atualizar Publicação: Atualizar uma publicação existente
    - Eliminar Publicação: Eliminar uma publicação existente
    - Listar Autores e suas Publicações: Listar autores e as suas respetivas publicações
    - Importar Publicações: Importar publicações de um arquivo JSON
    - Gerar Relatórios: Gerar relatórios de estatísticas
    - Analisar Publicações por Autor: Listar as publicações que contenham cada autor
    - Analisar Publicações por Palavra-Chave: Listar as publicações que contenham cada palavra-chave
    - Help: Exibir esta mensagem de ajuda
    - Sair: Sair do programa
    """
    sg.popup_scrolled("Ajuda", comandos)

# Executar GUI
if __name__ == "__main__":
    gui()

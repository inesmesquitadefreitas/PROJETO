import json
import FreeSimpleGUI as sg
import matplotlib.pyplot as plt

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
# Função para CRIAR uma nova publicação
def criarPublicacao():
    layout = [
        [sg.Text("Título:", text_color='black'), sg.InputText(key="titulo")],
        [sg.Text("Resumo:", text_color='black'), sg.Multiline(key="resumo")],
        [sg.Text("Palavras-chave (separadas por vírgulas):", text_color='black'), sg.InputText(key="palavras_chave")],
        [sg.Text("DOI:", text_color='black'), sg.InputText(key="doi")],
        [sg.Text("URL do PDF:", text_color='black'), sg.InputText(key="url_pdf")],
        [sg.Text("URL do Artigo:", text_color='black'), sg.InputText(key="url_artigo")],
        [sg.Text("Data de Publicação (YYYY-MM-DD):", text_color='black'), sg.InputText(key="data_publicacao")],
        [sg.Text("Autores e Afiliações:", text_color='black')],
        [sg.Button("Adicionar Autor", button_color=("black", "pink")), sg.Button("Remover Autor", button_color=("black", "pink"))],
        [sg.Listbox(values=[], size=(40, 5), key="autores", enable_events=True)],
        [sg.Button("Salvar", button_color=("white", "crimson")), sg.Button("Cancelar", button_color=("black", "pink"))],
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
# Função para CONSULTAR uma publicação específica
def consultarPublicacao():
    sg.theme('LightGrey1')
    layout = [
        [sg.Text("Digite o índice da publicação:"), sg.InputText(key="indice")],
        [sg.Button("Consultar", button_color=("white", "crimson")), sg.Button("Cancelar", button_color = ('black', 'pink'))],
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
# Função para FILTRAR publicações
def filtrarPublicacoes():
    layout1 = [
        [sg.Text("Escolha o tipo de filtro:", text_color='black')],
        [sg.Button("Título", button_color=("white", "crimson")),
         sg.Button("Autor", button_color=("white", "crimson")),
         sg.Button("Afiliação", button_color=("white", "crimson")),
         sg.Button("Data da Publicação", button_color=("white", "crimson")),
         sg.Button("Palavra-Chave", button_color=("white", "crimson")),
         sg.Button("Cancelar", button_color=("black", "pink"))],
        [sg.Multiline(size=(60, 15), key="resultado", disabled=True)],
    ]
    janela = sg.Window("Filtrar Publicações", layout1)

    cond1 = True
    while cond1:
        event, values = janela.read()
        if event in (sg.WINDOW_CLOSED, "Cancelar"):
            cond1 = False
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
                    layout2 = [
                        [sg.Text("Escolha o tipo de ordenação:")],
                        [sg.Button("Ordenar por ordem alfabética dos títulos", button_color=("white", "crimson"), key="titulo")],
                        [sg.Button("Ordenar por ordem de data de publicação", button_color=("white", "crimson"), key="data")],
                        [sg.Button("Cancelar", button_color=("black", "pink"))],
                    ]

                    janela2 = sg.Window("Ordenar Resultados", layout2)

                    cond2=True
                    while cond2:
                        event2, values2 = janela2.read()
                        
                        if event2 in (sg.WINDOW_CLOSED, "Cancelar"):
                            cond2=False
                        elif event2 == "titulo":
                            publicacoes_encontradas.sort(key=lambda x: x.get("title", "").lower())
                        elif event2 == "data":
                            publicacoes_encontradas.sort(key=lambda x: x.get("publish_date", ""), reverse=True)
                        
                        resultado = "\n\n".join([
                        f"Título: {p.get('title', 'N/A')}\nAutores: {', '.join([a['name'] for a in p.get('authors', [])])}\nData: {p.get('publish_date', 'N/A')}" for p in publicacoes_encontradas
                        ])
                        janela["resultado"].update(resultado)
                        cond2 = False

                    janela2.close()

                else:
                    sg.popup("Nenhuma publicação encontrada.")

    janela.close()

# ----------------------------------------------------------------------
# Função para ATUALIZAR uma publicação existente ✔
def atualizarPublicacao():
    layout1 = [
        [sg.Text("Índice da publicação a atualizar:"), sg.InputText(key="indice")], # o input será o valor da chave "indice" (dicionário)
        [sg.Button("Atualizar", button_color=("white", "crimson")), sg.Button("Cancelar", button_color=("black", "pink"))],
    ]

    janela1 = sg.Window("Consultar Publicação", layout1)

    continuar = True
    while continuar:
        event, values = janela1.read()

        if event in (sg.WINDOW_CLOSED, "Cancelar"): # sg.WINDOW_CLOSED --> utilizador clicar no X (canto superior direito)
            continuar = False
            janela1.close()

        elif event == "Atualizar":
            try:
                indice = int(values["indice"])
                if 0 <= indice < len(dados):
                    publicacao = dados[indice]

                    janela1.close() # Fechar a janela de consulta antes de abrir a próxima
                    continuar = False

                    layout2 = [
                        [sg.Text("Título:"), sg.InputText(publicacao.get("title", ""), key="titulo")],
                        [sg.Text("Resumo:"), sg.Multiline(publicacao.get("abstract", ""), key="resumo")],
                        [sg.Text("Palavras-chave (separadas por vírgulas):"), sg.InputText(publicacao.get("keywords", ""), key="palavras_chave")],
                        [sg.Text("Data de Publicação (YYYY-MM-DD):"), sg.InputText(publicacao.get("publish_date", ""), key="data_publicacao")],
                        [sg.Text("Autores e Afiliações:")],
                        [sg.Listbox(values=[f"{a['name']} ({a['affiliation']})" for a in publicacao.get("authors", [])],
                                    size=(40, 5), key="autores", enable_events=True)],
                        [sg.Text("(Se desejar editar ou remover autor, selecione o nome do mesmo na lista.)")],
                        [sg.Button("Adicionar Autor", button_color=("black", "pink")), sg.Button("Editar Autor", button_color=("black", "pink")), sg.Button("Remover Autor", button_color=("black", "pink"))],
                        [sg.Button("Salvar", button_color=("black", "green")), sg.Button("Cancelar", button_color=("black", "pink"))],
                    ]

                    janela2 = sg.Window("Atualizar Publicação", layout2)
                    
                    autores = publicacao.get("authors", [])
                    atualizar = True
                    while atualizar:
                        event_atualizar, values_atualizar = janela2.read()

                        if event_atualizar in (sg.WINDOW_CLOSED, "Cancelar"):
                            atualizar = False
                            janela2.close()
                        
                        elif event_atualizar == "Adicionar Autor":
                            nome_autor = sg.popup_get_text("Nome do Autor:")
                            afiliacao = sg.popup_get_text(f"Afiliação de {nome_autor}:")
                            if nome_autor and afiliacao:
                                autores.append({"name": nome_autor, "affiliation": afiliacao})
                                janela2["autores"].update(
                                    [f"{a['name']} ({a['affiliation']})" for a in autores]
                                )
                        
                        elif event_atualizar == "Editar Autor":
                            selecionado = values_atualizar["autores"]
                            if selecionado:
                                selecionado_texto = selecionado[0]
                                nome_existente, afiliacao_existente = selecionado_texto.split(" (")
                                afiliacao_existente = afiliacao_existente.rstrip(")")
                                novo_nome = sg.popup_get_text("Editar Nome do Autor:", default_text=nome_existente)
                                nova_afiliacao = sg.popup_get_text("Editar Afiliação do Autor:", default_text=afiliacao_existente)
                                if novo_nome and nova_afiliacao:
                                    for autor in autores:
                                        if autor["name"] == nome_existente and autor["affiliation"] == afiliacao_existente:
                                            autor["name"] = novo_nome
                                            autor["affiliation"] = nova_afiliacao
                                            break
                                    janela2["autores"].update(
                                        [f"{a['name']} ({a['affiliation']})" for a in autores]
                                    )
                        
                        elif event_atualizar == "Remover Autor":
                            selecionado = values_atualizar["autores"]
                            if selecionado:
                                autores = [
                                    a for a in autores if f"{a['name']} ({a['affiliation']})" not in selecionado
                                ]
                                janela2["autores"].update(
                                    [f"{a['name']} ({a['affiliation']})" for a in autores]
                                )

                        elif event_atualizar == "Salvar":
                            publicacao["title"] = values_atualizar["titulo"]
                            publicacao["abstract"] = values_atualizar["resumo"]
                            publicacao["keywords"] = values_atualizar["palavras_chave"]
                            publicacao["publish_date"] = values_atualizar["data_publicacao"]
                            publicacao["authors"] = autores

                            salvarDados(dados)
                            sg.popup("Publicação atualizada com sucesso!")
                            atualizar = False
                            janela2.close()
                else:
                    sg.popup_error("Índice inválido!")
            except ValueError:
                sg.popup_error("Por favor, insira um número válido.")

# ----------------------------------------------------------------------
# Função para ELIMINAR uma publicação ✔
def eliminarPublicacao():
    layout = [
        [sg.Text("Índice da publicação a eliminar:"), sg.InputText(key="indice")],
        [sg.Button("Eliminar", button_color=("white", "crimson")), sg.Button("Cancelar", button_color=("black", "pink"))],
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
# Função para listar AUTORES e as suas PUBLICAÇÕES ✔
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
                        autor_publicacoes[nome_autor].append(p['title'])
                    else:
                        autor_publicacoes[nome_autor].append("Publicação sem Título.")

    with open("listaAutoresPublicacoes.txt", "w", encoding="utf-8") as f:
        f.write("------ AUTORES E RESPETIVAS PUBLICAÇÕES ------\n")
        for autor, publicacoes in autor_publicacoes.items():
            f.write(f"\nAutor: {autor}\n")
            f.write("Publicações:\n")
            for pub in publicacoes:
                f.write(f"  - {pub}\n")
            f.write("\n")

    sg.popup("Lista de autores e as suas respetivas publicações foi gerada com sucesso em 'listaAutoresPublicacoes.txt'.")

# ----------------------------------------------------------------------
# Função para IMPORTAR dados de outro arquivo JSON ✔
def importarDados():
    layout = [
        [sg.Text("Selecione o arquivo JSON para importar:"), sg.Input(key="-FILE-"), sg.FileBrowse(file_types=(('JSON Files', '*.json'),))],
        [sg.Button("Importar", button_color=("white", "crimson"), key="-IMPORTAR-"), sg.Button("Cancelar", button_color=("black", "pink"))],
    ]

    window = sg.Window("Importar Dados", layout)

    cond = True
    while cond:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Cancelar"):
            cond = False
        elif event == "-IMPORTAR-":
            ficheiro = values["-FILE-"]
            if ficheiro:
                try:
                    with open(ficheiro, encoding='utf-8') as f:
                        novos_dados = json.load(f)
                        dados.extend(novos_dados)
                        salvarDados(dados)
                        sg.popup(f"Dados importados com sucesso do ficheiro {ficheiro}!")
                except Exception as e:
                    sg.popup_error(f"Erro ao importar dados: {e}")
            else:
                sg.popup("Erro", "Por favor, selecione um arquivo JSON para importar.")

    window.close()
    
# ----------------------------------------------------------------------
# Função para gerar RELATÓRIOS de ESTATÍSTICAS
def gerarRelatorios():
    layout = [
        [sg.Text("Escolha o relatório que deseja gerar:", text_color='crimson', font=("Arial", 16, "bold"))],
        [sg.Button("Distribuição de Publicações por Ano", button_color=("black", "pink"), key="1")],
        [sg.Button("Distribuição de Palavras-Chave por Frequência", button_color=("black", "pink"), key="2")],
        [sg.Button("Distribuição de Publicações Por Autor", button_color=("black", "pink"), key="3")],
        [sg.Button("Distribuição de Publicações por Mês de um Ano", button_color=("black", "pink"), key="4")],
        [sg.Button("Distribuição de Publicações de um Autor por Anos", button_color=("black", "pink"), key="5")],
        [sg.Button("Distribuição de Palavra-Chave Mais Frequente por Ano", button_color=("black", "pink"), key="6")],
        [sg.Button("Sair", button_color=("white", "crimson"), key="7")],
    ]

    window = sg.Window("Gerar Relatórios de Estatísticas", layout, size = (400, 300), finalize=True)

    with open("relatorio.md", "w", encoding="utf-8") as f:
        f.write("RELATÓRIO DE ESTATÍSTICAS\n")

    cond = True
    while cond:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED or event == "7":
            cond = False

        if event == "1":
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

            anos = [x[0] for x in anos_ordenados]
            contagem_publicacoes = [x[1] for x in anos_ordenados]

            # Gerar Gráfico de Barras Verticais
            plt.bar(anos, contagem_publicacoes, color="tomato")
            plt.xlabel("Anos", weight='bold', labelpad = 10)
            plt.ylabel("Número de Publicações", weight='bold', labelpad = 10)
            plt.title("Distribuição de Publicações por Ano", weight='bold')
            plt.xticks(rotation=45, ha='right')  # Rotaciona os anos em 45 graus e alinha à direita
            plt.tight_layout() # Ajusta automaticamente os elementos do gráfico para evitar sobreposição

            for i in range(len(anos)):
            # Ajusta posição do texto dinamicamente
                posicao_y = contagem_publicacoes[i] + 2
                plt.text(
                    x=anos[i], 
                    y=posicao_y,  # Posição ajustada
                    s=str(contagem_publicacoes[i]),  # Texto a ser exibido
                    ha='center',  # Alinhamento horizontal
                    fontsize=8,
                    color="black"
                )
            
            grafico1 = "publicacoesPorAno.png"
            plt.savefig(grafico1)

            with open("relatorio.md", "a", encoding="utf-8") as f: # "a" --> add (se escrevesse "w", apagava tudo o que o ficheiro já tinha)
                f.write("\nNúmero de publicações por ano\n")
                for ano, contagem_publicacoes in anos_ordenados:
                    f.write(f"- {ano}: {contagem_publicacoes}\n")
                f.write("\n")
                f.write(f"![Gráfico de Distribuição de Publicações por Ano]({grafico1})\n")
            
            plt.show()
            plt.close()
            sg.popup(f"Relatório gerado com sucesso em 'relatorio.md'.")

          
        elif event == "2":
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

            grafico2 = "frequenciaPalavrasChave.png"
            plt.savefig(grafico2)

            with open("relatorio.md", "a", encoding="utf-8") as f:
                f.write("\nFrequência de palavras-chave:\n")
                for palavra, frequencia in top20_palavras:
                    f.write(f"- {palavra}: {frequencia}\n")
                f.write("\n")
                f.write(f"![Gráfico de Frequências de Palavras-Chave]({grafico2})\n")
        
            plt.show()
            plt.close()
            sg.popup(f"Relatório gerado com sucesso em 'relatorio.md'.")

        elif event == "3":
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

            grafico3 = "publicacoesPorAutor.png"
            plt.savefig(grafico3)

            with open("relatorio.md", "a", encoding="utf-8") as f:
                f.write("\nNúmero de publicações por autor:\n")
                for nomes, n_publicacoes in top20_autores:
                    f.write(f"- {nomes}: {n_publicacoes}\n")
                f.write("\n")
                f.write(f"![Gráfico de Distribuição de Publicações Por Autor]({grafico3})\n")

            plt.show()
            plt.close()
            sg.popup(f"Relatório gerado com sucesso em 'relatorio.md'.")

        elif event == "4":
            layout = [
                [sg.Text("Digite o ano para análise:")],
                [sg.Input(key="-ANO-", size=(10, 1))],
                [sg.Button("OK"), sg.Button("Cancelar")]
            ]
            window = sg.Window("Seleção de Ano", layout)
            event, values = window.read()
            if event == "OK" and values["-ANO-"].isdigit():
                ano_escolhido = int(values["-ANO-"])
                window.close()
                
            else:
                sg.popup("Ano inválido ou cancelado.")
                window.close()

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

            grafico4 = f"publicacoesPorMesde{ano_escolhido}.png"
            plt.savefig(grafico4)
    
            with open("relatorio.md", "a", encoding="utf-8") as f:
                f.write(f"\nNúmero de Publicações por Mês em {ano_escolhido}:\n")
                for mes, publicacoes in contagem_meses.items():
                    f.write(f"- {mes}: {publicacoes}\n")
                f.write("\n")
                f.write(f"![Gráfico de Distribuição de Publicações Por Mês em {ano_escolhido}]({grafico4})\n")

            plt.show()
            plt.close()
            sg.popup(f"Relatório gerado com sucesso em 'relatorio.md'.")

        elif event == "5":
            autores = list(set(autor["name"] for p in dados if p.get("authors") for autor in p["authors"]))
            layout = [
                [sg.Text("Escolha o autor para análise:")],
                [sg.Combo(autores, size=(30, 1), key="-AUTOR-")],
                [sg.Button("OK"), sg.Button("Cancelar")]
            ]
            window = sg.Window("Seleção de Autor", layout)
            event, values = window.read()
            if event == "OK" and values["-AUTOR-"]:
                autor_escolhido = values["-AUTOR-"]
                window.close()
   
            else:
                sg.popup("Autor inválido ou cancelado.")
                window.close()

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

            grafico5 = f"publicacoesPorMesde{autor_escolhido}.png"
            plt.savefig(grafico5)

            # Escrever Relatório
            with open("relatorio.md", "a", encoding="utf-8") as f:
                f.write(f"\nNúmero de Publicações por Anos de {autor_escolhido}:\n")
                for anos, quantidades in anos_ordenados:
                    f.write(f"- {anos}: {quantidades}\n")
                f.write("\n")
                f.write(f"![Gráfico de Distribuição de Publicações Por Mês de {autor_escolhido}]({grafico5})\n")

            plt.show()
            plt.close()
            sg.popup(f"Relatório gerado com sucesso em 'relatorio.md'.")
    

        elif event == "6":
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
            plt.legend(handles=handles, ncol=3, loc="lower right", fontsize=10, title="Palavra Mais Frequente por Ano")

            # Configurar títulos e rótulos
            plt.xlabel("Anos", fontsize=12, weight='bold', labelpad=12)
            plt.ylabel("Frequência da Palavra-Chave", fontsize=12, weight='bold', labelpad=12)
            plt.title("Palavra-Chave Mais Frequente por Ano", fontsize=14, weight='bold')
            plt.xticks(anos, rotation=45)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()

            grafico6 = "palavraChaveFrequentePorAno.png"
            plt.savefig(grafico6)

            # Escrever o relatório
            with open("relatorio.md", "a", encoding="utf-8") as f:
                f.write("\nPalavra-chave mais frequente por ano:\n")
                for ano, (palavra, frequencia) in palavras_frequentes_por_ano.items():
                    f.write(f"- {ano}: {palavra} ({frequencia} ocorrências)\n")
                f.write("\n")
                f.write(f"![Gráfico de Palavra-Chave mais Frequente por Ano]({grafico6})\n")

            plt.show()
            plt.close()

            sg.popup(f"Relatório gerado com sucesso em 'relatorio.md'.")
            cond = False

    window.close()

# ----------------------------------------------------------------------
# Função para ANÁLISE de PUBLICAÇÕES por AUTOR ✔
def analisePublicacoesAutor():
    dicionario_autores = {}

    for p in dados:
        if p.get('authors'):
            for autor in p["authors"]:
                if autor.get('name'):
                    nome_autor = autor["name"]
                    if nome_autor not in dicionario_autores:
                        dicionario_autores[nome_autor] = []
                    dicionario_autores[nome_autor].append(p)

    # Layout da interface gráfica
    layout = [
        [sg.Text("Escolha o tipo de ordenação:")],
        [sg.Button("Ordenar por frequência de artigos publicados (ordem decrescente)", button_color=("white", "crimson"), key="-FREQUENCIA-")],
        [sg.Button("Ordenar por ordem alfabética dos nomes dos autores", button_color=("white", "crimson"), key="-ALFABETICA-")],
        [sg.Button("Cancelar", button_color=("black", "pink"))]
    ]

    # Janela da aplicação utilizando a biblioteca FreeSimpleGUI
    window = sg.Window("Análise de Publicações por Autor", layout)

    cond = True
    while cond:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Cancelar"):
            cond = False
        elif event == "-FREQUENCIA-":
            autores_ordenados = sorted(dicionario_autores.items(), key=lambda x: len(x[1]), reverse=True)
        elif event == "-ALFABETICA-":
            autores_ordenados = sorted(dicionario_autores.items(), key=lambda x: x[0].lower())

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

        sg.popup("Sucesso", "Análise de publicações por autor gerada com sucesso em 'analisePublicacoesAutores.txt'.")
        cond = False

    window.close()
# ----------------------------------------------------------------------
# Função para análise de PUBLICAÇÕES por PALAVRA-CHAVE ✔
def analisePublicacoesPalavraChave():
    dicionario_palavras = {}

    for p in dados:
        if p.get('keywords'):
            listaKeywords = [palavra.strip(". ") for palavra in p['keywords'].split(", ")]
            for palavra in listaKeywords:
                if palavra not in dicionario_palavras:
                    dicionario_palavras[palavra] = []
                dicionario_palavras[palavra].append(p)

    layout = [
        [sg.Text("Escolha o tipo de ordenação:")],
        [sg.Button("Ordenar palavras-chave pela frequência de ocorrências (ordem decrescente)", button_color=("white", "crimson"), key="-FREQUENCIA-")],
        [sg.Button("Ordenar palavras-chave por ordem alfabética", button_color=("white", "crimson"), key="-ALFABETICA-")],
        [sg.Button("Cancelar", button_color=("black", "pink"))]
    ]

    window = sg.Window("Análise de Publicações por Palavra-Chave", layout)

    cond = True
    while cond:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Cancelar"):
            cond = False
        elif event == "-FREQUENCIA-":
            palavras_ordenadas = sorted(dicionario_palavras.items(), key=lambda x: len(x[1]), reverse=True)
        elif event == "-ALFABETICA-":
            palavras_ordenadas = sorted(dicionario_palavras.items(), key=lambda x: x[0])

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

        sg.popup("Sucesso", "Análise de publicações por palavra-chave gerada com sucesso em 'analisePublicacoesPalavrasChave.txt'.")
        cond = False

    window.close()
    
# ----------------------------------------------------------------------
# Função principal para o menu de linha de comando

# Menu Principal
def menu_principal():
    sg.theme("LightGrey1") # cor do fundo
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
         sg.Button("Help", button_color=("black", "lightblue"))],
        [sg.Button("Sair", button_color=("white", "crimson"))],
    ]
    return sg.Window("Menu Principal", layout, finalize=True)

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
            importarDados()
        elif event == "Gerar Relatórios":
            gerarRelatorios()
        elif event == "Analisar Publicações por Autor":
            analisePublicacoesAutor()
        elif event == "Analisar Publicações por Palavra-Chave":
            analisePublicacoesPalavraChave()
        elif event == "Help":
            exibirHelp()
    janela.close()

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

# Executar
if __name__ == "__main__":
    gui()
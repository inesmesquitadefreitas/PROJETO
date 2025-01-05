# Relatório do Projeto

## Sistema de Consulta e Análise de Publicações Científicas

### Algoritmos e Técnicas de Programação
### Docentes: José Carlos Ramalho e Luís Filipe Cunha

#### Ana Teresa Ribeiro, A107202 (a107202@uminho.pt)
#### Beatriz Maia Oliveira, A107281 (a107281@uminho.pt)
#### Inês Mesquita de Freitas, A108959 (a108959@uminho.pt)

### Introdução

O presente relatório descreve a elaboração de um projeto realizado no âmbito da unidade curricular “Algoritmos e Técnicas de Programação”, cujo objetivo é desenvolver, em Python, um “Sistema de Consulta e Análise de Publicações Científicas”. 
Para tal, foram utilizadas estruturas de dados apropriadas e as bibliotecas necessárias para o correto funcionamento da aplicação. Para uma interação mais intuitiva, foi ainda utilizada uma interface gráfica, o FreeSimpleGUI, que permite a visualização de um menu que apresenta as funções disponíveis.

### Descrição do Projeto
O projeto permite criar, atualizar e analisar publicações científicas. Com base num dataset de publicações, o sistema possibilita a pesquisa de artigos utilizando filtros, como a data de publicação, as palavras-chave, autores, entre outros. Adicionalmente, são também gerados relatórios que exibem gráficos ilustrativos e pormenorizados, com estatísticas para a análise de métricas dos artigos e dos seus autores.

#### Requisitos do Sistema
O sistema deve incorporar as seguintes funções:

1. Carregamento da Base de Dados: O programa deverá inicialmente carregar para memória o dataset guardado no ficheiro de suporte à aplicação (ataMedicaPapers.json);

2. Criação de Publicações: O utilizador deverá conseguir criar um novo artigo, definindo um título, um resumo, as palavras-chave, o DOI (digital object identifier), uma lista de autores e a sua afiliação correspondente, o url para o ficheiro PDF do artigo, a data de publicação e o url do artigo; 

3. Atualização de Publicações: O sistema deverá possibilitar a atualização da informação de uma publicação, nomeadamente a data de publicação, o resumo, as palavras-chave, os autores e as afiliações; 

4. Consulta de Publicações: O sistema deverá permitir pesquisar publicações, através de filtros, sendo estes o título, um autor, uma afiliação, a data de publicação e as palavras-chave. Deverá ainda ser possível ordenar as publicações encontradas pelos títulos e pela data de publicação; 

5. Análise de Publicações por Autor : O sistema deverá facultar a listagem dos autores e aceder aos artigos de cada autor da lista. Os autores devem aparecer ordenados pela frequência dos seus artigos publicados e/ou por ordem alfabética; 

6. Análise de Publicações por Palavras-chave: O sistema deverá permitir a pesquisa e visualização das palavras-chave do dataset, devendo estas estar ordenadas pelo seu número de ocorrências nos artigos e/ou por ordem alfabética. Para além disso, o sistema deverá também permitir visualizar a lista das publicações associadas a cada palavra-chave; 

7. Estatísticas de Publicação: O sistema deverá apresentar relatórios que incluam os seguintes gráficos: 
* Distribuição de publicações por ano;
* Distribuição de publicações por mês de um determinado ano;
* Número de publicações por autor (top 20 autores); 
* Distribuição de publicações de um autor por anos; 
* Distribuição de palavras-chave pela sua frequência (top 20 palavras-chave); 
* Distribuição de palavras-chave mais frequente por ano.

8. Armazenamento dos Dados: Quando o utilizador decidir sair da aplicação ou tiver selecionado o armazenamento dos dados, a aplicação deverá guardar os dados em memória no ficheiro de suporte; 

9. Importação de Dados: Em qualquer momento, deverá ser possível importar novos registos de um outro ficheiro que tenha a mesma estrutura do ficheiro de suporte; 

10. Exportação parcial de dados: Em qualquer momento, deverá ser possível exportar para ficheiro os registos resultantes de uma pesquisa.

#### Requisitos Técnicos
Os principais objetivos deste projeto incluem:
- Implementar o sistema da aplicação em Python;
- Utilizar estruturas de dados apropriadas para armazenar a informação sobre as publicações;
- Desenvolver duas interfaces: uma de linha de comando (CLI) e uma gráfica (GUI);
- Integrar bibliotecas Python para funcionalidades gráficas, como Matplotlib;
- Implementar um mecanismo de armazenamento persistente, como um ficheiro JSON.


### Desenvolvimento da Aplicação
#### Estrutura de Dados
O código da aplicação utiliza as seguintes estruturas de dados: dicionários, listas e listas de dicionários. O sistema consiste numa lista de dicionários, correspondendo cada um destes dicionários a uma publicação. Esta inclui diversas categorias: resumo (“abstract”), palavras-chave (“keywords”), DOI (“doi”), url do pdf (“pdf”), data de publicação (“publish_date”), título (“title”), url do artigo (“url”) e autores (“authors”), correspondendo estes, por sua vez, a uma lista de dicionários que compreendem o nome (“name”) e a afiliação do(s) autor(es) (“affiliation”).
Adicionalmente, a biblioteca JSON é utilizada para salvar e guardar os dados das publicações, assim como aceder a dados já existentes nesse arquivo.
Por fim, a utilização do FreeSimpleGUI facilitou a criação de interfaces gráficas de forma simples e intuitiva, visto que permite a visualização da linha de comando num menu claro e acessível. Este exibe as funções de criar, consultar, filtrar, atualizar, eliminar, importar publicações, assim como as de listar autores e as suas publicações, gerar relatórios, analisar publicações por autor e, finalmente, analisar publicações por palavra-chave.

#### Linhas de Comando
Um utilizador da interface de linha de comandos poderá executar as seguintes opções presentes no menu:
* Criar Publicação: adiciona uma nova publicação, com a introdução de todas as informações inerentes à mesma;
* Consultar Publicação: encontra uma publicação através do seu índice;
* Filtrar Publicações: lista publicações que obedecem a determinados filtros, entre eles, o título, autor, afiliação, palavras-chave e data de publicação;
* Atualizar Publicação: atualiza uma publicação existente, substituindo a informação por uma nova que foi introduzida;
* Eliminar Publicação: apaga uma publicação existente;
* Listar Autores e as suas Publicações: lista autores e as suas respectivas publicações;
* Importar Publicações: importa publicações de um arquivo JSON;
* Gerar Relatórios: elabora relatórios de estatísticas;
* Analisar Publicações por autor: lista as publicações de um determinado autor;
* Analisar Publicações por palavra-chave: lista as publicações que contenham uma determinada palavra-chave;
* Help: exibe uma mensagem de ajuda com os comandos disponíveis;
* Sair: termina o programa.

#### Explicação do Código
Função para Carregar os Dados:
- A função **carregaDados** tem como propósito carregar os dados armazenados num arquivo JSON para o uso no programa. Relativamente ao parâmetro *fnome*, este representa o nome ou o caminho JSON, com um valor padrão, neste caso, definido como “ata_medica_papers.json”. Isto permite que a função seja usada sem a necessidade de especificar o arquivo sempre que seja necessário utilizá-la.
- Quanto ao funcionamento desta função, esta abre o arquivo JSON no modo de leitura com a codificação “utf-8” para garantir a compatibilidade com caracteres especiais e, de seguida, utiliza o métodos json.load para converter o conteúdo do arquivo JSON num objeto Python, como um dicionário ou uma lista.
- Esta função possui, ainda, tratamento para possíveis erros. Se o arquivo não existir ou o conteúdo do arquivo JSON não for válido, esta irá retornar um dicionário vazio e irá exibir mensagens de erro. Em caso de sucesso, a função retorna os dados carregados do arquivo. 

Função para Salvar Dados:
- A função **salvarDados**, tem como objetivo salvar os dados num arquivo JSON.
- Esta recebe dois parâmetros:
  * dados - são os dados a serem salvos em formato de dicionário ou lista;
  * ficheiro - nome ou caminho do arquivo onde os dados são armazenados (padrão: “ata_medica_papers.json”).
- O seu funcionamento consiste na abertura do arquivo no modo e escrita (“w”) com a codificação “utf-8” e salvar os dados utilizando json.dump, formatando-os com indent=4 para maior legibilidade. Caso ocorra algum erro durante o processo, uma mensagem detalhada é exibida ao usuário para informar o problema.

Função Main:
- A função **main** controla o fluxo principal do programa, organizando as operações de carregar, visualizar e salvar os dados.
- Em primeiro lugar, utiliza a função **carregaDADOS** para carregar os dados de um ficheiro JSON localizado no caminho especificado, armazenando-os na variável dados.
- De seguida, exibe os dados carregados com o comando *print*, permitindo verificar se estes foram carregados corretamente. Por fim, chama a função **salvarDados** para gravar os dados no ficheiro JSON. 

Função do Menu Principal
- A função **menu_principal** é responsável por criar e retornar a interface gráfica de um menu principal, utilizando a biblioteca FreeSimpleGUI. Esta função organiza a interface através de um conjunto de botões, cada um com uma funcionalidade específica, e elementos, para facilitar a interação do utilizador com o programa.

Função principal GUI:
- A função *gui* encarrega-se por implementar a interface gráfica do usuário (GUI) principal do programa;
- Esta utiliza o FreeSimpleGUI para exibir a janela inicial e gerir as interações do usuário com o menu principal;
- A função chama a função menu_principal para criar o layout e retornar a janela do menu principal;
- O programa entra num loop contínuo que processa as ações geradas pelo utilizador, como os cliques nos botões das opções do menu;
- Dentro do loop, a função verifica qual o botão que foi selecionado ou se a janela foi fechada;
- Independentemente da ação, a função executa a atividade correspondente;
- Caso o usuário selecione a opção "Sair" ou feche a janela no canto superior direito, o programa encerra o loop e fecha a janela.

Função para Criar uma Publicação
- A função **criarPublicacao** tem o intuito de permitir ao usuário criar uma nova publicação com detalhes como o título, resumo, palavras-chave, autores, DOI, links e data de publicação. Estes dados introduzidos pelo utilizador são então salvos e armazenados na lista de publicações do arquivo JSON, *ataMmedicaPapers.json*.
- Para tal, seleciona-se na janela do Menu Principal a opção “Criar Publicação”, que abre uma nova janela, onde é possível inserir as informações necessárias.
- Por fim, uma mensagem *pop-up* confirma que a publicação foi salva com sucesso.

Função para Consultar uma Publicação Específica:
- A função **consultarPublicacao** permite ao utilizador consultar os detalhes de uma publicação específica, identificada pelo índice na lista de publicações. Esta funcionalidade utiliza a biblioteca *FreeSimpleGUI* para criar uma interface gráfica. 
- A função começa por definir o tema visual da janela como LightGrey1 e constrói um layout que inclui uma caixa de texto para introduzir o índice da publicação, botões para "Consultar" e "Cancelar", e uma área de texto, não editável, onde os detalhes da publicação serão exibidos, criando, em seguida, uma janela com este layout.
- Assim, o programa entra num ciclo onde lê os eventos da janela e os valores inseridos pelo utilizador. Caso o utilizador clique no botão "Cancelar" ou feche a janela, o ciclo termina, encerrando a janela. Se o botão "Consultar" for clicado, a função tenta converter o valor introduzido na caixa de texto para um número inteiro, que será utilizado como índice para aceder à publicação.
- Se o índice for válido (ou seja, estiver dentro dos limites da lista de publicações), a função recupera os dados da publicação correspondente e constrói uma string formatada com as informações, como o título, resumo, palavras-chave, DOI, autores e data de publicação, sendo estas informações apresentadas na área de texto da janela. Caso o índice seja inválido ou o valor introduzido não for um número, a função exibe uma mensagem de erro. 
- Por fim, quando o utilizador termina a consulta, a janela é fechada e a função encerra. Esta função é útil para explorar rapidamente os detalhes de uma publicação específica, utilizando uma interface amigável e mensagens claras para lidar com erros.


Função para Filtrar Publicações:
- A função **filtrarPublicacoes** permite que o utilizador pesquise publicações na base de dados com base em critérios específicos, utilizando uma interface gráfica criada com o *FreeSimpleGUI*. 
- A função inicia configurando o tema da janela e definindo um layout que inclui uma mensagem explicativa, botões para selecionar os critérios de filtro (como "Título", "Autor", "Afiliação", "Data da Publicação" e "Palavra-Chave") e uma área de texto para exibir os resultados. Um botão "Cancelar" também está disponível para sair do processo de filtragem.
- A janela é apresentada ao utilizador, e a função entra num ciclo que processa os eventos da interface. Se o utilizador fechar a janela ou clicar no botão "Cancelar", o ciclo termina e a janela é fechada. Caso o utilizador clique num dos botões de filtro, como "Título" ou "Autor", é exibida uma caixa de diálogo para introduzir o termo a ser pesquisado. O termo introduzido é guardado na variável filtro.
- Com base no filtro selecionado, a função percorre a lista de publicações (dados) e verifica se os critérios correspondem. As publicações que atendem ao critério são guardadas numa lista chamada publicacoes_encontradas. Caso sejam encontradas as publicações pretendidas, a função exibe os resultados formatados na área de texto da janela, incluindo o título, os nomes dos autores e a data de publicação. Se nenhuma publicação for encontrada, uma mensagem de aviso é exibida.
- Por fim, quando o utilizador termina a filtragem ou fecha a janela, o ciclo é encerrado, e a janela é fechada. Esta função é útil para localizar rapidamente publicações específicas na base de dados, fornecendo uma interface acessível e várias opções de pesquisa.

Função para atualizar uma publicação existente
- A função **atualizarPublicacao** é responsável por gerir a atualização de informações de uma publicação específica dentro de um conjunto de dados. Esta função utiliza a biblioteca FreeSimpleGUI para criar uma interface gráfica e fornecer etapas interativas para selecionar e editar uma publicação.
- Um layout (layout_consulta) é definido com um campo de entrada de texto para se inserir o índice da publicação que se deseja atualizar, e também os botões “Atualizar” e “Cancelar”. Caso o índice introduzido esteja dentro do intervalo válido de publicações na lista dados, a janela de consulta é fechada e um novo layout é criado para exibir os detalhes da publicação (título, resumo, palavras-chave, data de publicação), permitindo que o usuário atualize os campos.
- Os valores dos campos preenchidos pelo utilizador são capturados e usados para atualizar os detalhes da publicação no dicionário correspondente. Uma mensagem de confirmação de sucesso é exibida no ecrã.

Função para eliminar uma publicação existente:
- A função **eliminarPublicacao** permite ao utilizador eliminar uma publicação específica da lista de publicações, identificada pelo seu índice. A interface gráfica, criada com FreeSimpleGUI, guia o utilizador no processo de remoção.
- A função começa por definir o layout da janela, que inclui um campo de entrada para o índice da publicação a eliminar e dois botões: "Eliminar" e "Cancelar". Quando a janela é aberta, a função entra num ciclo onde lê os eventos e os valores introduzidos pelo utilizador.
- Se o utilizador clicar em "Cancelar" ou fechar a janela, o ciclo é terminado, e a janela é encerrada. Caso clique em "Eliminar", a função tenta converter o valor introduzido no campo de índice para um número inteiro. Em seguida, verifica se o índice é válido, ou seja, se está dentro do intervalo da lista de publicações (dados).
- Se o índice for válido, a função utiliza o método pop para remover a publicação correspondente da lista. Após a remoção, os dados atualizados são salvos no ficheiro JSON utilizando a função salvarDados, e uma mensagem de sucesso é exibida ao utilizador. Por outro lado, se o índice for inválido, ou se o valor introduzido não for um número, uma mensagem de erro é apresentada. Por fim, a janela é encerrada ao concluir a operação.

Função para listar autores e as suas publicações
- A função **listarAutores** tem como intuito criar um arquivo de texto que contenha uma lista de autores e as respetivas publicações registadas na estrutura de dados;
- A função percorre os dados, organiza as informações de cada autor e salva tudo num arquivo denominado por “listaAutoresPublicacoes.txt";
- O arquivo é aberto no modo de escrita (“w”) com a codificação UTF-8, para garantir a compatibilidade com caracteres especiais;
- Após gerar o arquivo, a função imprime a mensagem: "Lista de autores e as suas respetivas publicações gerada com sucesso em 'listaAutoresPublicacoes.txt'."

Função para importar dados:
- A função **importarDados** permite adicionar publicações de outro ficheiro JSON à base de dados existente. 
- A função recebe como parâmetro o nome ou o caminho de um ficheiro JSON (ficheiro);
- Utiliza um bloco try para lidar com possíveis erros durante o processo;
- Primeiro, abre o ficheiro especificado em modo de leitura, utilizando a codificação utf-8 para garantir compatibilidade com caracteres especiais;
- De seguida, carrega os dados do ficheiro como um objeto Python (como uma lista ou dicionário) usando json.load.
- Os dados importados são adicionados à base de dados existente, representada pela variável dados, utilizando o método extend, que insere múltiplos elementos no final de uma lista;
- Após a adição, os dados atualizados são salvos no ficheiro principal, recorrendo à função salvarDados;
- Se a importação for bem-sucedida, uma mensagem de sucesso é exibida no console, indicando que os dados foram importados corretamente;
- Se ocorrer algum erro durante o processo, como o ficheiro não existir ou ter um formato inválido, a função captura a exceção e imprime uma mensagem de erro detalhada.

Função para Gerar Relatórios de Estatísticas:
- A função **gerarRelatorios** é responsável por criar relatórios de estatísticas com base nos dados do ficheiro com o qual trabalhamos;
- Estes relatórios incluem distribuições de publicações por ano, palavras-chave por frequência, publicações por autor, entre outros, e apresentam visualizações como gráficos e resumos escritos num arquivo Markdown (*relatorio.md*);
- Esta utiliza o FreeSimpleGUI para apresentar um menu de opções, onde o usuário escolhe o tipo de relatório a ser gerado;
- As opções incluem diferentes análises, como:
  - Distribuição de publicações por ano;
  - Frequência de palavras-chave;
  - Distribuição de publicações por autor;
  - Distribuição de publicações por mês de um ano específico;
  - Distribuição de publicações de um autor específico por ano;
  - Palavra-chave mais frequente por ano.
- É posteriormente criado (ou atualizado) um arquivo chamado *relatorio.md* para armazenar os resultados num formato estruturado. As informações incluem descrições e links para gráficos salvos como imagens;
- Para cada opção, os dados são processados para gerar estatísticas e gráficos correspondentes;
- Os gráficos são salvos localmente e vinculados ao relatório no arquivo Markdown;
- Após gerar o relatório correspondente, o programa exibe uma mensagem de sucesso e permite ao usuário continuar ou sair.

Função para Análise de Publicações por Autor:
- A função **analisePublicacoesAutor** agrupa e analisa publicações com base nos autores listados no campo *authors*;
- Esta cria um dicionário (*dicionario_autores*) onde cada autor será uma chave, associada a uma lista de publicações;
- Ao percorrer cada publicação presente na lista do ficheiro *ataMedicaPapers.json*, esta verifica se a publicação contém autores, analisando-os e adicionando cada nome de autor (*name*) a *dicionario_palavras*, se este ainda não estiver lá presente;
- O valor associado a cada autor corresponde a uma lista que contém todas as publicações que este escreveu;
- A interface gráfica, implementada com FreeSimpleGUI, oferece duas opções de ordenação:
  - Por frequência de publicações (em ordem decrescente);
  - Por ordem alfabética dos nomes dos autores.
- Após a ordenação, os resultados são exportados para o ficheiro "analisePublicacoesAutores.txt", incluindo os nomes dos autores, o respetivo número de publicações e detalhes de cada publicação (título e data, se disponíveis);
- Quando terminada a análise, é exibida uma mensagem de sucesso.

Função para Análise de Publicações por Palavra-Chave:
- A função **analisePublicacoesPalavraChave** organiza e analisa publicações com base em palavras-chave extraídas do campo *keywords*;
- Esta cria um dicionário (*dicionario_palavras*) onde cada palavra-chave será uma chave, associada a uma lista de publicações;
- Ao percorrer cada publicação presente na lista do ficheiro *ataMedicaPapers.json*, esta verifica se a publicação contém palavras-chave, analisando-as e adicionando cada palavra a *dicionario_palavras*, se esta ainda não estiver lá presente;
- O valor associado a cada palavra corresponde a uma lista que contém todas as publicações que mencionam a palavra;
- A função vai permitir, depois, ao usuário, via interface gráfica com o FreeSimpleGUI, escolher a ordenação das palavras-chave:
  - Por frequência de ocorrências (ordem decrescente);
  - Por ordem alfabética.
- Após a ordenação, os resultados são salvos no ficheiro "analisePublicacoesPalavrasChave.txt", incluindo as palavras-chave, o respetivo número de ocorrências (tamanho da lista de publicações: *len(artigos)*) e detalhes das publicações (título e data, se disponíveis);
- Ao concluir a análise, é exibida uma mensagem de sucesso.
  
Função para Exibir *Help*:
- A função **exibirHelp** fornece uma descrição detalhada dos comandos disponíveis no programa, facilitando o uso por novos usuários ou para referência rápida.

### Exemplo de Execução do Sistema
(1) O utilizador seleciona, no menu, a funcionalidade que deseja implementar:
  
  ![Captura de ecrã 2025-01-05 181829](https://github.com/user-attachments/assets/83f7127a-2235-424a-abae-fa4d50897ea9)

(2) Após selecionar “Criar Publicação”, este preenche os campos necessários:
  
  ![Captura de ecrã 2025-01-05 184300](https://github.com/user-attachments/assets/589a75ff-6a78-4500-9560-3e4f5bea5a5a)


### Conclusão
Para conseguirmos desenvolver o “Sistema de Consulta e Análise de Publicações Científicas”, foi necessária a utilização de todos os conhecimentos previamente adquiridos, assim como a utilização de diversas informações disponibilizadas na internet para o cumprimento dos objetivos do projeto. 

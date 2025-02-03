import json
import requests
import tkinter as tk


def buscar_jogo(entry, text_widget):
    """
    Busca um jogo no arquivo JSON remoto, ordena os resultados alfabeticamente pelo título
    e exibe os resultados formatados no widget de texto.

    Args:
        entry (tk.Entry): Widget de entrada onde o usuário digita o nome do jogo.
        text_widget (tk.Text): Widget de texto onde os resultados serão exibidos.
    """
    texto = entry.get()  # Obtém o texto inserido pelo usuário

    # URL do arquivo JSON com os dados
    url = "https://raw.githubusercontent.com/KekitU/rutracker-hydra-links/main/all_categories.json"

    # Requisição HTTP para buscar os dados
    response = requests.get(url)
    data = response.json()

    # Filtra os downloads que contenham o texto digitado no título
    resultados = [
        item for item in data.get("downloads", [])
        if texto.lower() in item.get("title", "").lower()
    ]

    # Ordena os resultados alfabeticamente pelo título
    resultados_ordenados = sorted(resultados, key=lambda x: x.get("title", "").lower())

    # Formatação dos resultados
    resposta = formatar_resultados(resultados_ordenados)

    # Exibe o texto formatado no widget de texto
    exibir_resultados(resposta, text_widget)


def formatar_resultados(resultados):
    """
    Formata os resultados da busca em um texto legível.

    Args:
        resultados (list): Lista de dicionários contendo os dados dos jogos encontrados.

    Returns:
        str: Texto formatado com os resultados.
    """
    resposta = json.dumps(resultados, indent=2)

    # Substitui as chaves do JSON por nomes mais amigáveis
    resposta = (resposta
                .replace("{", "=" * 80)
                .replace("[", "")
                .replace("\"", "")
                .replace("]", "")
                .replace("}", "")
                .replace(",", "")
                .replace("uris:", "Link Torrent:")
                .replace("uploadDate:", "Data de upload:")
                .replace("fileSize:", "Tamanho:")
                .replace("repackLinkSource:", "Fonte:")
                .replace("title", "Titulo"))

    return resposta


def exibir_resultados(resposta, text_widget):
    """
    Exibe os resultados formatados no widget de texto.

    Args:
        resposta (str): Texto formatado com os resultados da busca.
        text_widget (tk.Text): Widget de texto onde os resultados serão exibidos.
    """
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)  # Limpa o Text antes de adicionar novo conteúdo
    text_widget.insert(tk.END, resposta)
    text_widget.config(state=tk.DISABLED)

    # Ajusta a altura do widget de texto com base no número de linhas
    linhas = resposta.count("\n") + 1
    text_widget.config(height=min(linhas, 2000))


def criar_janela():
    """
    Cria e configura a interface gráfica da aplicação.
    """
    janela = tk.Tk()
    janela.title("Buscar Games")
    janela.columnconfigure(0, weight=1)

    # Fonte para os resultados
    fonte_resposta = ("Arial", 12, "bold")

    # Widgets da interface
    texto_orientacao = tk.Label(janela, text="Digite o jogo que quer buscar:")
    texto_orientacao.grid(column=0, row=0, sticky="w")

    txt_box_pesquisa = tk.Entry(janela, width=50)
    txt_box_pesquisa.grid(column=0, row=1, sticky="ew")

    botao = tk.Button(janela, text="Pesquisar", command=lambda: buscar_jogo(txt_box_pesquisa, text_saida))
    botao.grid(column=0, row=2, sticky="w")

    # Frame e área de texto para resultados
    frame_texto = tk.Frame(janela)
    frame_texto.grid(column=0, row=3, sticky="nsew")
    janela.rowconfigure(3, weight=1)

    scrollbar = tk.Scrollbar(frame_texto, orient="vertical")
    text_saida = tk.Text(frame_texto, height=5, wrap="word", yscrollcommand=scrollbar.set, font=fonte_resposta)
    text_saida.pack(side="left", fill="both", expand=True)

    # Desabilita a edição no widget de texto
    text_saida.config(state=tk.DISABLED)

    # Estilo do botão
    botao.config(border="3px")

    janela.mainloop()


if __name__ == "__main__":
    criar_janela()

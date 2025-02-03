import json
import requests
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QScrollArea

def buscar_jogo(entry, text_widget):
    """
    Busca um jogo no arquivo JSON remoto, ordena os resultados alfabeticamente pelo título
    e exibe os resultados formatados no widget de texto.

    Args:
        entry (QLineEdit): Widget de entrada onde o usuário digita o nome do jogo.
        text_widget (QTextEdit): Widget de texto onde os resultados serão exibidos.
    """
    texto = entry.text()  # Obtém o texto inserido pelo usuário

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
                .replace("title", "Título"))

    return resposta


def exibir_resultados(resposta, text_widget):
    """
    Exibe os resultados formatados no widget de texto.

    Args:
        resposta (str): Texto formatado com os resultados da busca.
        text_widget (QTextEdit): Widget de texto onde os resultados serão exibidos.
    """
    text_widget.setPlainText(resposta)


def criar_janela():
    """
    Cria e configura a interface gráfica da aplicação.
    """
    app = QApplication([])

    janela = QWidget()
    janela.setWindowTitle("Buscar Games")

    # Layout principal
    layout = QVBoxLayout()

    # Texto de orientação
    texto_orientacao = QLabel("Digite o jogo que quer buscar:")
    layout.addWidget(texto_orientacao)

    # Caixa de texto para pesquisa
    txt_box_pesquisa = QLineEdit()
    txt_box_pesquisa.setPlaceholderText("Digite o nome do jogo...")
    layout.addWidget(txt_box_pesquisa)

    # Botão de pesquisa
    botao = QPushButton("Pesquisar")
    botao.clicked.connect(lambda: buscar_jogo(txt_box_pesquisa, text_saida))
    layout.addWidget(botao)

    # Área de texto para mostrar resultados
    text_saida = QTextEdit()
    text_saida.setReadOnly(True)

    # ScrollArea para o widget de texto
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(text_saida)

    layout.addWidget(scroll_area)

    janela.setLayout(layout)
    janela.resize(600, 400)
    janela.show()

    app.exec_()


if __name__ == "__main__":
    criar_janela()

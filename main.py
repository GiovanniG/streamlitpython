import streamlit as st
from datetime import datetime
import pytz
import mysql.connector
from decouple import config

# Função para verificar se uma string é um número decimal com ponto ou está vazia
def is_decimal_or_empty(s):
    if s.strip() == "":
        return True
    try:
        # Verifique se a string pode ser convertida em float usando ponto como separador decimal
        float(s)
        return True
    except ValueError:
        return False

# Função para exibir informações formatadas em HTML
def exibir_informacoes(parametro_selecionado, parametros, comentario, data_atual, hora_atual):
    info_html = ""
    info_html += f'<p><strong>Localidade Selecionada:</strong> {parametro_selecionado}</p>'
    for i, parametro in enumerate(parametros, start=1):
        info_html += f'<p><strong>Parâmetro {i}:</strong> {parametro}</p>'
    info_html += f'<p><strong>Comentário:</strong> {comentario}</p>'
    info_html += f'<p><strong>Data:</strong> {data_atual}</p>'
    info_html += f'<p><strong>Hora:</strong> {hora_atual}</p>'
    return info_html

# Lê as variáveis de ambiente do arquivo .env
DB_HOST = config('DB_HOST')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_DATABASE = config('DB_DATABASE')
DB_PORT = config('DB_PORT')

# Define a função criar_conexao para criar uma conexão com o banco de dados
def criar_conexao():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        port=DB_PORT
    )

st.set_page_config(page_title="Controle Operacional")

def main():
    # Divida a página em duas colunas
    col1, col2 = st.columns(2)

    # Mensagem de aviso entre "Controle Operacional" e "Selecione a localidade"
    with col1:
        st.markdown(
            f'<div style="text-align:center;">'
            f'<h2 style="font-weight: bold;">Controle Operacional</h2>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.warning("Os campos de 1 a 6 devem conter apenas números (use ponto como separador decimal) ou permanecer em branco.\n\n"
                 "Caso queira consultar a dashboard com todos os dados, [clique aqui](https://app.powerbi.com/view?r=eyJrIjoiMGJhODM2ODctMDg2My00MTU1LThmYTAtYmFkYTRhYjg4Yzg3IiwidCI6ImIxZWQ2ZjZkLWI2ZDAtNGI5MS04ZGUwLTEzYzc1ZWQ0OTBhMiJ9).\n\n"
                 "A dashboard é atualizada a cada 3h, começando às 0h.")

    # Na primeira coluna (col1), adicione um seletor antes de "Parâmetro 1" com as opções
    with col1:
        # Adicione um seletor (dropdown) para escolher uma opção
        opcoes = ["#92", "BW Datakon", "Caldeira", "Chillers Catenárias"]
        parametro_selecionado = st.selectbox("Selecione a localidade:", opcoes)

        # Adicione um parâmetro de entrada para "Parâmetro 1"
        parametro1 = st.text_input("Parâmetro 1:")

        # Adicione um parâmetro de entrada para "Parâmetro 2"
        parametro2 = st.text_input("Parâmetro 2:")

        # Adicione um parâmetro de entrada para "Parâmetro 3"
        parametro3 = st.text_input("Parâmetro 3:")

        # Adicione um parâmetro de entrada para "Parâmetro 4"
        parametro4 = st.text_input("Parâmetro 4:")

        # Adicione um parâmetro de entrada para "Parâmetro 5"
        parametro5 = st.text_input("Parâmetro 5:")

        # Adicione um parâmetro de entrada para "Parâmetro 6"
        parametro6 = st.text_input("Parâmetro 6:")

        # Adicione um parâmetro de entrada para "Comentário"
        comentario = st.text_input("Comentário:")

        # Quando o botão "Enviar" for clicado, verifique se os campos de 1 a 6 contêm apenas números com ponto como separador decimal
        if st.button("Enviar"):
            if not all(is_decimal_or_empty(parametro) for parametro in [parametro1, parametro2, parametro3, parametro4, parametro5, parametro6]):
                st.error("Os campos de 1 a 6 devem conter apenas números (use ponto como separador decimal) ou permanecer em branco.")
            else:
                # Obtenha a data e a hora atual em São Paulo
                tz = pytz.timezone('America/Sao_Paulo')
                data_hora_atual = datetime.now(tz)

                # Separe as informações de data e hora em colunas diferentes
                data_atual = data_hora_atual.strftime("%Y-%m-%d")
                hora_atual = data_hora_atual.strftime("%H:%M:%S")

                # Determine a tabela a ser usada com base na opção selecionada
                tabela = ""
                if parametro_selecionado == "#92":
                    tabela = "92_Trafilas_Al"

                if tabela:
                    # Agora você pode usar a função criar_conexao para conectar-se ao banco de dados e
                    # realizar operações de banco de dados, se necessário.
                    conexao = criar_conexao()
                    # Exemplo de consulta SQL com nomes de colunas correspondentes
                    cursor = conexao.cursor()
                    cursor.execute(
                        f"INSERT INTO {tabela} (Codigo, Data, Hora, pH, Salinidade, Condutividade_Eletrica, Turbidez, Comentario) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (parametro_selecionado, data_atual, hora_atual, parametro1, parametro2, parametro3, parametro4, comentario))
                    conexao.commit()
                    conexao.close()

                    # Use st.markdown para aplicar o estilo com borda e exibir informações ao usuário
                    st.markdown(
                        f'<div style="border: 1px solid #ccc; '
                        f'padding: 20px; border-radius: 10px; '
                        f'box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">'
                        f'<h3>Informações do Cliente</h3>'
                        f'{exibir_informacoes(parametro_selecionado, [parametro1, parametro2, parametro3, parametro4, parametro5, parametro6], comentario, data_atual, hora_atual)}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    # Exibe a mensagem de sucesso
                    st.success("Dados gravados com sucesso.")

    # Na segunda coluna (col2), adicione a tabela sem o "Parâmetro 7"
    with col2:
        dados_tabela = [
            ["Código", "Parâmetro 1", "Parâmetro 2", "Parâmetro 3", "Parâmetro 4", "Parâmetro 5", "Parâmetro 6"],
            ["#92", "pH", "Salinidade (ppt)", "Condutividade elétrica (uS/cm)", "Turbidez (NTU)", "-", "-"],
            ["BW Datakon", "pH", "Salinidade (ppt)", "Condutividade elétrica (uS/cm)", "Turbidez (NTU)", "-", "-"],
            ["Caldeira", "pH", "Salinidade (ppt)", "Condutividade elétrica (uS/cm)", "Turbidez (NTU)", "-", "-"],
            ["Chillers Catenárias", "Cloro", "pH", "Temperatura", "Turbidez (NTU)", "-", "-"]
        ]

        # Título acima da tabela
        st.write("Quadro de parâmetros e respectivas unidades")

        # Use st.markdown para personalizar o estilo da tabela e remover os índices
        tabela_html = "<table><tr><th>{}</th></tr>{}</table>".format(
            "</th><th>".join(dados_tabela[0]),
            "</tr><tr>".join("<td>{}</td>".format("</td><td>".join(map(str, row))) for row in dados_tabela[1:])
        )

        # Adicionar a tabela com o título
        st.markdown(tabela_html, unsafe_allow_html=True)

        # Legenda no canto inferior esquerdo da tabela
        st.text("FONTE: AUTOR, 2023.")

if __name__ == "__main__":
    main()

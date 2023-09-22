import streamlit as st
import re
from datetime import datetime
import pytz
import mysql.connector

# Define a função criar_conexao para criar uma conexão com o banco de dados
def criar_conexao():
    return mysql.connector.connect(
        host="containers-us-west-60.railway.app",
        user="root",
        password="U5dsl1BkLfAUbHwjsoVY",
        database="railway",
        port=5823
    )

st.set_page_config(page_title="Cadastro de Clientes")

def main():
    # Centraliza o título "Cadastro de Clientes" usando CSS
    st.markdown(
        f'<div style="text-align:center;">'
        f'<h1>Cadastro de Clientes</h1>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Adiciona um campo de entrada para o nome
    nome = st.text_input("Nome:")

    # Adiciona um campo de entrada para o CPF
    cpf = st.text_input("CPF:")

    # Quando o botão "Enviar" for clicado, exibe as informações ou mensagens de erro
    if st.button("Enviar"):
        # Verifica se o campo de nome foi preenchido e não está vazio
        if not nome:
            st.warning("O campo Nome não pode estar vazio.")
            return  # Encerra a função se o campo de nome estiver vazio

        # Expressão regular para verificar se o campo nome não contém números
        nome_valido = bool(re.match(r'^\D*$', nome))

        # Expressão regular para verificar se o campo CPF contém apenas números e tem 11 caracteres
        cpf_valido = bool(re.match(r'^\d{11}$', cpf))

        if nome_valido and cpf_valido:
            # Obtém a data e a hora atual em São Paulo
            tz = pytz.timezone('America/Sao_Paulo')
            data_hora_atual = datetime.now(tz)

            # Separa as informações de data e hora em colunas diferentes
            data_atual = data_hora_atual.strftime("%Y-%m-%d")
            hora_atual = data_hora_atual.strftime("%H:%M:%S")

            # Agora você pode usar a função criar_conexao para conectar-se ao banco de dados e
            # realizar operações de banco de dados, se necessário.
            conexao = criar_conexao()
            # Exemplo de consulta SQL com colunas de data e hora separadas
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO clientes (nome, cpf, data, hora) "
                           "VALUES (%s, %s, %s, %s)", (nome, cpf, data_atual, hora_atual))
            conexao.commit()
            conexao.close()

            # Use st.markdown para aplicar o estilo com borda e exibir informações ao usuário
            st.markdown(
                f'<div style="border: 1px solid #ccc; '
                f'padding: 20px; border-radius: 10px; '
                f'box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">'
                f'<h3>Informações do Cliente</h3>'
                f'<p><strong>Nome:</strong> {nome}</p>'
                f'<p><strong>CPF:</strong> {cpf}</p>'
                f'<p><strong>Data:</strong> {data_atual}</p>'
                f'<p><strong>Hora:</strong> {hora_atual}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

            # Exibe a mensagem de sucesso
            st.success("Dados gravados com sucesso.")

        else:
            if not nome_valido:
                st.warning("O campo Nome não pode conter números.")
            if not cpf_valido:
                st.warning("O campo CPF deve conter exatamente 11 números.")

if __name__ == "__main__":
    main()

import streamlit as st
import re
from datetime import datetime
import pytz
import mysql.connector

# Defina as variáveis globais 'nome' e 'cpf' como strings vazias inicialmente
nome = ""
cpf = ""

# Função para criar a conexão com o banco de dados MySQL
def criar_conexao():
    return mysql.connector.connect(
        host="containers-us-west-200.railway.app",
        user="root",
        password="DNmptpDcP8c5Hmy0bn72",
        database="railway",
        protocol="TCP"
    )

st.set_page_config(page_title="Cadastro de Clientes")

def main():
    global nome, cpf  # Use a palavra-chave 'global' para indicar que estamos usando as variáveis globais 'nome' e 'cpf'

    # ...

    # Quando o botão "Enviar" for clicado, exibe as informações ou mensagens de erro
    if st.button("Enviar"):
        # Verifica se o campo de nome foi preenchido e não está vazio
        if not nome:
            st.warning("O campo Nome não pode estar vazio.")
            st.text("Fluxo de execução: Nome vazio")
            return  # Encerra a função se o campo de nome estiver vazio

        # Expressão regular para verificar se o campo nome não contém números
        nome_valido = bool(re.match(r'^\D*$', nome))
        st.text(f"Debug: nome_valido = {nome_valido}")

        # Expressão regular para verificar se o campo CPF contém apenas números e tem 11 caracteres
        cpf_valido = bool(re.match(r'^\d{11}$', cpf))
        st.text(f"Debug: cpf_valido = {cpf_valido}")

        if nome_valido and cpf_valido:
            # Cria uma conexão com o banco de dados MySQL
            conexao = criar_conexao()
            cursor = conexao.cursor()

            # Insira a lógica para interagir com o banco de dados aqui, por exemplo, executar uma inserção
            try:
                inserir_dados = "INSERT INTO tabela_exemplo (nome, cpf) VALUES (%s, %s)"
                valores = (nome, cpf)
                cursor.execute(inserir_dados, valores)
                conexao.commit()

                # Use st.markdown para aplicar o estilo com borda
                st.markdown(
                    f'<div style="border: 1px solid #ccc; '
                    f'padding: 20px; border-radius: 10px; '
                    f'box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">'
                    f'<h3>Informações do Cliente</h3>'
                    f'<p><strong>Nome:</strong> {nome}</p>'
                    f'<p><strong>CPF:</strong> {cpf}</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                st.text("Fluxo de execução: Dados gravados com sucesso")

            except mysql.connector.Error as err:
                st.error(f"Erro ao inserir dados no banco de dados: {err}")
                st.text("Fluxo de execução: Erro ao inserir dados no banco de dados")

            finally:
                cursor.close()
                conexao.close()

            # Obtém a data e a hora atual em São Paulo
            tz = pytz.timezone('America/Sao_Paulo')
            data_hora_atual = datetime.now(tz).strftime("%d/%m/%Y às %H:%M:%S")
            # Exibe a mensagem de sucesso com a data e hora
            st.success(f"Dados gravados com sucesso em {data_hora_atual}.")
            st.text("Fluxo de execução: Sucesso")

        else:
            if not nome_valido:
                st.warning("O campo Nome não pode conter números.")
                st.text("Fluxo de execução: Nome inválido")
            if not cpf_valido:
                st.warning("O campo CPF deve conter exatamente 11 números.")
                st.text("Fluxo de execução: CPF inválido")

if __name__ == "__main__":
    main()

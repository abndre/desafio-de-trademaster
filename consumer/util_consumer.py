import json
import os
import uuid
import psycopg2
from datetime import datetime

# Função para salvar a mensagem no arquivo
def save_message(message, success=True, path='01-raw'):
    path = f'./data/{path}/event/msg/' if success else f'./data/{path}/fail/msg/'
    os.makedirs(path, exist_ok=True)
    filename = f'{str(uuid.uuid4())}_{datetime.now().strftime("%Y-%m-%d")}_.json'
    filepath = os.path.join(path, filename)
    with open(filepath, 'w') as file:
        json.dump(message, file)
    print("Mensagem salva em:", filepath)


def check_content_message(body):
    # Configuração da conexão PostgreSQL
    postgres_connection = psycopg2.connect(
        host='localhost',
        port='5432',
        database='mydb',
        user='postgres',
        password='postgres'
    )
    postgres_cursor = postgres_connection.cursor()

    try:
        # Converter a mensagem para um dicionário
        # Decode the message from bytes to a string
        message = body.decode('utf-8').replace("'", '"')

        # Parse the message as JSON
        dados_aluguel_venda = json.loads(message)

        # Raw data
        save_message(dados_aluguel_venda, success=True, path='01-raw')


        # Obter os IDs de cliente, funcionário e item
        id_evento = dados_aluguel_venda['id_evento']
        id_cliente = dados_aluguel_venda['id_cliente']
        id_funcionario = dados_aluguel_venda['id_funcionario']
        id_item = dados_aluguel_venda['id_item']

        # Validar se o cliente existe
        postgres_cursor.execute("SELECT id_cliente FROM Cliente WHERE id_cliente = %s", (id_cliente,))
        cliente_exists = postgres_cursor.fetchone() is not None

        dados_aluguel_venda['has_id_client'] = cliente_exists

        # Validar se o funcionário existe
        postgres_cursor.execute("SELECT id_funcionario FROM Funcionario WHERE id_funcionario = %s", (id_funcionario,))
        funcionario_exists = postgres_cursor.fetchone() is not None

        dados_aluguel_venda['has_id_funcionario'] = funcionario_exists

        # Validar se o item existe
        postgres_cursor.execute("SELECT id_item FROM Item WHERE id_item = %s", (id_item,))
        item_exists = postgres_cursor.fetchone() is not None

        dados_aluguel_venda['has_id_item'] = item_exists

        # Verificar se todos os dados existem
        if cliente_exists and funcionario_exists and item_exists:
            # Salvar a mensagem no banco de dados (exemplo de inserção)
            postgres_cursor.execute("INSERT INTO Aluguel_Venda (id_cliente, id_funcionario, id_item, data_evento, data_devolucao, evento) VALUES (%s, %s, %s, %s, %s,%s)", (id_cliente, id_funcionario, id_item, dados_aluguel_venda['data_aluguel'], dados_aluguel_venda['data_devolucao'], id_evento))
            postgres_connection.commit()

            # Salvar a mensagem no arquivo de sucesso
            save_message(dados_aluguel_venda, success=True, path='02-processed')
        else:
            # Salvar a mensagem no arquivo de falha
            save_message(dados_aluguel_venda, success=False, path='02-processed')

    except Exception as e:
        # Se ocorrer algum erro, salvar a mensagem no arquivo de falha
        save_message(dados_aluguel_venda, success=False, path='02-processed')
        print("Erro ao processar mensagem:", str(e))

    # finally:
    #     # Confirmar o recebimento da mensagem
    #     ch.basic_ack(delivery_tag=method.delivery_tag)
    return message
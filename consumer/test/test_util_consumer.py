import unittest
from unittest.mock import patch, MagicMock
from util_consumer import save_message, check_content_message

class TestUtilConsumer(unittest.TestCase):

    def test_save_message_success(self):
        message = {'id': 1, 'content': 'Test message'}
        path = 'test'
        with patch('util_consumer.os.makedirs') as mock_makedirs, \
             patch('util_consumer.uuid.uuid4', return_value='test_uuid'), \
             patch('util_consumer.datetime') as mock_datetime, \
             patch('util_consumer.json.dump') as mock_dump:

            mock_datetime.now().strftime.return_value = '2021-01-01'
            save_message(message, success=True, path=path)

            mock_makedirs.assert_called_once_with(f'./data/{path}/event/msg/', exist_ok=True)
            mock_dump.assert_called_once_with(message, mock_dump.return_value.__enter__.return_value)

    def test_check_content_message_success(self):
        body = b'{"id_evento": 1, "id_cliente": 1, "id_funcionario": 1, "id_item": 1, "data_aluguel": "2021-01-01", "data_devolucao": "2021-01-02"}'
        cursor_mock = MagicMock()
        cursor_mock.fetchone.return_value = (1,)
        cursor_mock.execute.return_value = None

        connection_mock = MagicMock()
        connection_mock.cursor.return_value.__enter__.return_value = cursor_mock

        with patch('util_consumer.json.loads') as mock_json_loads, \
             patch('util_consumer.save_message') as mock_save_message, \
             patch('util_consumer.psycopg2.connect', return_value=connection_mock):

            mock_json_loads.return_value = {
                'id_evento': 1,
                'id_cliente': 1,
                'id_funcionario': 1,
                'id_item': 1,
                'data_aluguel': '2021-01-01',
                'data_devolucao': '2021-01-02'
            }

            result = check_content_message(body)

            mock_json_loads.assert_called_once_with(body.decode('utf-8').replace("'", '"'))
            cursor_mock.execute.assert_has_calls([
                MagicMock('SELECT id_cliente FROM Cliente WHERE id_cliente = %s', (1,)),
                MagicMock('SELECT id_funcionario FROM Funcionario WHERE id_funcionario = %s', (1,)),
                MagicMock('SELECT id_item FROM Item WHERE id_item = %s', (1,))
            ])
            mock_save_message.assert_called_once_with(
                mock_json_loads.return_value, success=True, path='raw'
            )
            self.assertEqual(result, body.decode('utf-8').replace("'", '"'))

if __name__ == '__main__':
    unittest.main()

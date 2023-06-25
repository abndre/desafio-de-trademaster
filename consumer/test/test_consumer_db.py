import unittest
import json
import os
from consumer_db import save_message, check_content_message


class ConsumerDBTestCase(unittest.TestCase):

    def test_save_message(self):
        # Define a sample message
        message = {'id': 1, 'text': 'Hello, world!'}

        # Call the save_message method
        save_message(message, success=True)

        # Verify if the file was created
        # You can modify this path according to your file structure
        file_path = './data/msg/'
        file_name = os.listdir(file_path)[0]
        self.assertEqual(file_name.endswith('.json'), True)

    def test_check_content_message(self):
        # Define a sample message
        message = json.dumps({
            'id_evento': 1,
            'id_cliente': 1,
            'id_funcionario': 1,
            'id_item': 1,
            'data_aluguel': '2023-06-25',
            'data_devolucao': '2023-07-02'
        }).encode('utf-8')

        # Call the check_content_message method
        result = check_content_message(message)

        # Verify if the message processing was successful
        self.assertEqual(result, message.decode('utf-8'))



if __name__ == '__main__':
    unittest.main()

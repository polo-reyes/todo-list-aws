# from pprint import pprint
import unittest
import warnings
import json
import os
import sys
import boto3
from botocore.exceptions import ClientError
from moto import mock_dynamodb

@mock_dynamodb
class TestDatabaseFunctions(unittest.TestCase):
    def setUp(self):
        print ('---------------------')
        print ('Start: setUp')
        warnings.filterwarnings(
            "ignore",
            category=ResourceWarning,
            message="unclosed.*<socket.socket.*>")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="callable is None.*")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="Using or importing.*")
        """Create the mock database and table"""
        try:
            self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            self.is_local = 'true'
            self.uuid = "123e4567-e89b-12d3-a456-426614174000"
            self.text = "Aprender DevOps y Cloud en la UNIR"

            from src.todoList import create_todo_table
            self.table = create_todo_table(self.dynamodb)
            #self.table_local = create_todo_table()
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print ('End: setUp')

    def tearDown(self):
        print ('---------------------')
        print ('Start: tearDown')
        """Delete mock database and table after test is run"""
        try:
            self.table.delete()
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print ('Table deleted succesfully')
            #self.table_local.delete()
            self.dynamodb = None
            print ('End: tearDown')

    def test_table_exists(self):
        print ('---------------------')
        print ('Start: test_table_exists')
        #self.assertTrue(self.table)  # check if we got a result
        #self.assertTrue(self.table_local)  # check if we got a result

        print('Table name:' + self.table.name)
        try:
            tableName = os.environ['DYNAMODB_TABLE'];
            # check if the table name is 'ToDo'
            self.assertIn(tableName, self.table.name)
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print ('End: test_table_exists')
        

    def test_put_todo(self):
        print ('---------------------')
        print ('Start: test_put_todo')
        # Testing file functions
        try:
            from src.todoList import put_item

            # Table local
            response = put_item(self.text, self.dynamodb)
            print ('Response put_item:' + str(response))
            self.assertEqual(200, response['statusCode'])
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print ('End: test_put_todo')

    def test_put_todo_error(self):
        print ('---------------------')
        print ('Start: test_put_todo_error')
        # Testing file functions
        try:
            from src.todoList import put_item

            # Table mock
            self.assertRaises(Exception, put_item("", self.dynamodb))
            self.assertRaises(Exception, put_item("", self.dynamodb))
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print ('End: test_put_todo_error')

    def test_get_todo(self):
        print ('---------------------')
        print ('Start: test_get_todo')
        try:
            from src.todoList import get_item, put_item

            # Testing file functions
            # Table mock
            responsePut = put_item(self.text, self.dynamodb)
            print ('Response put_item:' + str(responsePut))
            idItem = json.loads(responsePut['body'])['id']
            print ('Id item:' + idItem)
            self.assertEqual(200, responsePut['statusCode'])
            responseGet = get_item(
                    idItem,
                    self.dynamodb)
            print ('Response Get:' + str(responseGet))
            self.assertEqual(
                self.text,
                responseGet['text'])
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print ('End: test_get_todo')
    
    def test_list_todo(self):
        print ('---------------------')
        print ('Start: test_list_todo')
        try:
            from src.todoList import get_items, put_item

            # Testing file functions
            # Table mock
            put_item(self.text, self.dynamodb)
            result = get_items(self.dynamodb)
            print ('Response GetItems' + str(result))
            self.assertTrue(len(result) == 1)
            self.assertTrue(result[0]['text'] == self.text)
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print ('End: test_list_todo')


    def test_update_todo(self):
        print ('---------------------')
        print ('Start: test_update_todo')
        try:
            from src.todoList import get_item, put_item, update_item
            updated_text = "Aprender más cosas que DevOps y Cloud en la UNIR"
            # Testing file functions
            # Table mock
            responsePut = put_item(self.text, self.dynamodb)
            print ('Response PutItem' + str(responsePut))
            idItem = json.loads(responsePut['body'])['id']
            print ('Id item:' + idItem)
            result = update_item(idItem, updated_text,
                                "false",
                                self.dynamodb)
            print ('Result Update Item:' + str(result))
            self.assertEqual(result['text'], updated_text)
        except ClientError as error:
            print(error.response['Error']['Message'])
        else:
            print ('End: test_update_todo')


    def test_update_todo_error(self):
        print ('---------------------')
        print ('Start: atest_update_todo_error')
        try:            
            from src.todoList import put_item, update_item
            updated_text = "Aprender más cosas que DevOps y Cloud en la UNIR"
            # Testing file functions
            # Table mock
            responsePut = put_item(self.text, self.dynamodb)
            print ('Response PutItem' + str(responsePut))
            self.assertRaises(
                Exception,
                update_item(
                    updated_text,
                    "",
                    "false",
                    self.dynamodb))
            self.assertRaises(
                TypeError,
                update_item(
                    "",
                    self.uuid,
                    "false",
                    self.dynamodb))
            self.assertRaises(
                Exception,
                update_item(
                    updated_text,
                    self.uuid,
                    "",
                    self.dynamodb))
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print ('End: atest_update_todo_error')

    def test_delete_todo(self):
        print ('---------------------')
        print ('Start: test_delete_todo')
        try:
            from src.todoList import delete_item, get_items, put_item

            # Testing file functions
            # Table mock
            responsePut = put_item(self.text, self.dynamodb)
            print ('Response PutItem' + str(responsePut))
            idItem = json.loads(responsePut['body'])['id']
            print ('Id item:' + idItem)
            delete_item(idItem, self.dynamodb)
            print ('Item deleted succesfully')
            self.assertTrue(len(get_items(self.dynamodb)) == 0)
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print ('End: test_delete_todo')

    def test_delete_todo_error(self):
        print ('---------------------')
        print ('Start: test_delete_todo_error')
        try:
            from src.todoList import delete_item

            # Testing file functions
            self.assertRaises(TypeError, delete_item("", self.dynamodb))
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print ('End: test_delete_todo_error')



if __name__ == '__main__':
    unittest.main()
    

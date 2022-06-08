import os
import boto3
import time
import uuid
import json
import functools
from botocore.exceptions import ClientError


def get_table(dynamodb=None):
    try:
        if not dynamodb:
            URL = os.environ['ENDPOINT_OVERRIDE']
            if URL:
                print('URL dynamoDB:'+URL)
                boto3.client = functools.partial(
                    boto3.client,
                    endpoint_url=URL
                )
                boto3.resource = functools.partial(
                    boto3.resource,
                    endpoint_url=URL
                )
            dynamodb = boto3.resource("dynamodb")
        # fetch todo from the database
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    except ClientError as e:
        print(e.response['Error']['Message'])
        table = None
    else:
        print('Result getTable:' + table.name)
    return table


def get_item(key, dynamodb=None):
    try:
        table = get_table(dynamodb)
        result = table.get_item(
            Key={
                'id': key
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        result['Item'] = None
    else:
        print('Result getItem:' + str(result))
    return result['Item']


def get_items(dynamodb=None):
    try:
        table = get_table(dynamodb)
        result = table.scan()
    except ClientError as e:
        print(e.response['Error']['Message'])
        result['Items'] = None
    else:
        print('Result getItem:' + str(result))
    return result['Items']


def put_item(text, dynamodb=None):
    try:
        table = get_table(dynamodb)
        timestamp = str(time.time())
        print('Table name:' + table.name)
        item = {
            'id': str(uuid.uuid1()),
            'text': text,
            'checked': False,
            'createdAt': timestamp,
            'updatedAt': timestamp,
        }
        # write the todo to the database
        table.put_item(Item=item)
        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(item)
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
    return response


def update_item(key, text, checked, dynamodb=None):
    try:
        table = get_table(dynamodb)
        timestamp = int(time.time() * 1000)
        # update the todo in the database
        result = table.update_item(
            Key={
                'id': key
            },
            ExpressionAttributeNames={
              '#todo_text': 'text',
            },
            ExpressionAttributeValues={
              ':text': text,
              ':checked': checked,
              ':updatedAt': timestamp,
            },
            UpdateExpression='SET #todo_text = :text, '
                             'checked = :checked, '
                             'updatedAt = :updatedAt',
            ReturnValues='ALL_NEW',
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        result['Attributes'] = None
    return result['Attributes']


def delete_item(key, dynamodb=None):
    try:
        table = get_table(dynamodb)
        # delete the todo from the database
        table.delete_item(
            Key={
                'id': key
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    return


def create_todo_table(dynamodb):
    try:
        # For unit testing
        tableName = os.environ['DYNAMODB_TABLE']
        print('Creating Table with name:' + tableName)
        table = dynamodb.create_table(
            TableName=tableName,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        # Wait until the table exists.
        table.meta.client.get_waiter('table_exists').wait(TableName=tableName)
        if (table.table_status != 'ACTIVE'):
            raise AssertionError()
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print('Result getItem:' + table.name)
    return table

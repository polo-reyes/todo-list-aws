# -*- coding: utf-8 -*-

import json
import decimalencoder
import todoList
import boto3


def translate(event, context):
    translate = boto3.client(service_name='translate',
                             region_name='us-east-1',
                             use_ssl=True)
    if (event['pathParameters']['language']! = ''):
        langTarget = event['pathParameters']['language']
    else:
        langTarget = "en"
    
    item = todoList.get_item(event['pathParameters']['id'])
    print(item)
    textoAObtenerPorID = item['text']
    valor_traducido = translate.translate_text(Text=textoAObtenerPorID,
                                               SourceLanguageCode="auto",
                                               TargetLanguageCode=langTarget)
    print(valor_traducido.get('TranslatedText'))  

    response = {
        "statusCode": 200,
        "body": json.dumps(valor_traducido,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response

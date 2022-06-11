# -*- coding: utf-8 -*-

import json
import decimalencoder
import todoList
import boto3


def isLatin(textoTraducido):
    try:
        textoTraducido.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def translate(event, context):
    #call to translate
    translate = boto3.client(service_name='translate',
                             region_name='us-east-1',
                             use_ssl=True)
    #catching the arguments from event
    if (event['pathParameters']['language']! = ''):
        langTarget = event['pathParameters']['language']
    else:
        langTarget = "en"
    
    item = todoList.get_item(event['pathParameters']['id'])
    print(item)
    textoAObtenerPorID = item['text']
    #translating the text gotten by the get_item call
    valor_traducido = translate.translate_text(Text=textoAObtenerPorID,
                                               SourceLanguageCode="auto",
                                               TargetLanguageCode=langTarget)
    print(valor_traducido.get('TranslatedText'))
    #checking if translated text is latin-based
    isLatin(valor_traducido.get('TranslatedText'))

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(valor_traducido,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
import json
import decimalencoder
import todoList
import boto3

def translate(event, context):
    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
    valor_traducido = translate.translate_text(Text=event['pathParameters']['text'], SourceLanguageCode="eng", TargetLanguageCode="es")
    print(valor_traducido.get('TranslatedText'));
    return valor_traducido.get('TranslatedText')


import boto3
import json


def detect_text(bucket_name, filename):


    # Amazon Textract client
    textract = boto3.client('textract')

    # Call Amazon Textract   
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': filename
            }
        })

    #print(response)
    text = ''
    # Print detected text
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            text = text +' '+ (item["Text"])

    return text

def detect_language_and_translate(text):
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
    translate = boto3.client('translate')
    language = comprehend.detect_dominant_language(Text = text)
    language_code= language['Languages'][0]['LanguageCode']
    print(language_code)
    if language_code == "en":
        return text
    else:
        result = translate.translate_text(Text=text, SourceLanguageCode=language_code, TargetLanguageCode="en")
        return (result.get('TranslatedText'))

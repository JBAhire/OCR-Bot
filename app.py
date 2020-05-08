import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import pipeline
from s3_upload import upload
from detect import detect_text
import os

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms():
    bucket_name="add your bucket name"
    resp = MessagingResponse()
    filename = request.values['MessageSid'] + '.jpg'
    with open(filename, 'wb') as f:
        image_url = request.values['MediaUrl0']
        f.write(requests.get(image_url).content)
        upload(filename, bucket_name, filename)
        text = detect_text(bucket_name, filename)
        #translated_text = detect_language_and_translate(text)
        #print(translated_text)        
        resp.message(text)
        #resp.message(translated_text)        
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

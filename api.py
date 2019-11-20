
from datetime import datetime, date
from werkzeug.utils import secure_filename
import os
from flask import Flask, flash, request, redirect, url_for, jsonify
import requests
from flask_cors import CORS, cross_origin
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing import sequence
import numpy as np
from flask import Response
import pickle

app = Flask(__name__)
CORS(app, support_credentials=True)
model = load_model('textbasicLSTMmodel.h5')

with open("person2_data_collected.pickle","rb" ) as handle:
    data2 = pickle.load(handle)

text = []
for ses_mod in data2:
    text.append(ses_mod['transcription'])

MAX_SEQUENCE_LENGTH = 20
tokenizer = Tokenizer()
tokenizer.fit_on_texts(text)
token_tr_X = tokenizer.texts_to_sequences(text)


def pred(message):
    MAX_SEQUENCE_LENGTH=20
    emotions_used = np.array(['ang', 'hap', 'neu', 'sad','sur','fea'])
    
    test_text=[message]
    print(test_text)
    
    token_tr_X = tokenizer.texts_to_sequences(test_text)
    x_test_text = []
    x_test_text = sequence.pad_sequences(token_tr_X, maxlen=MAX_SEQUENCE_LENGTH)
    pred=model.predict(x_test_text)
    for i in pred:
        emotion = np.argmax(i)
        # print(emotions)
        print("Emotion Predicted:",emotion,emotions_used[emotion])
        return emotion,emotions_used[emotion]

@app.route('/sendmsg/<string:message>', methods =['GET','POST','DELETE','PUT'])
@cross_origin(supports_credentials=True)
def send_message(message):
    if(request.method=='GET'):
        print("post")
        print(message)
        x,y=pred(message)
        # print(x)
        print("y:",y)
        return Response(y, mimetype='text/xml')
    else:
        return Response("", mimetype='text/xml')


if(__name__=="__main__"):
    app.run(host='0.0.0.0', port=5050)
    

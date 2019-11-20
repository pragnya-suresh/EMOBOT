from datetime import datetime, date
from werkzeug.utils import secure_filename
import os
from flask import Flask, flash, request, redirect, url_for, jsonify, Response, json
import requests
from flask_cors import CORS, cross_origin
import numpy as np
from time import sleep
import csv
import random

app = Flask(__name__)
CORS(app, support_credentials=True)


prev=0
curr=0

@app.route('/comments', methods =['GET','POST','DELETE','PUT'])
@cross_origin(supports_credentials=True)
def send_comments():
    id = request.args["id"]
    print(id)
    csv_file = open("Output"+id+".csv","r")
    csv_reader = list(csv.DictReader(csv_file))
    print(len(csv_reader))
    if(request.method=='GET'):
        print("hi")
        def read_file():
            global prev
            global curr
            if(curr==99):
                prev=0;
                curr=0;
            
            x = random.randint(3,9)
            print(x)
            curr=curr+x
            pos_sent = 0
            neg_sent = 0
            comments=[]
            while(prev<curr):
                print(csv_reader[prev]["Comment"])
                comments.append(csv_reader[prev]['Comment'])
                senti = float(csv_reader[prev]["sentiment"])
                if(senti >= 0):
                     pos_sent += 1
                else:
                    neg_sent += 1
                prev+=1
            print(pos_sent,neg_sent)
            comments.append(pos_sent)
            comments.append(neg_sent)
            yield json.dumps(comments)
            sleep(10)
        return Response(read_file(),mimetype="text/json")
    else:
        return jsonify(), 405


if(__name__=="__main__"):
    app.run(host='0.0.0.0', port=5000)



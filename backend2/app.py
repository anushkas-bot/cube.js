# app.py
from flask import Flask, render_template, jsonify
import requests
import logging
import json
import pymongo
from pymongo import MongoClient
from flask_sqlalchemy import SQLAlchemy
from localStoragePy import localStoragePy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

cluster = MongoClient("mongodb+srv://anushka:4OcHQ3QwKKhc33aL@cluster0.70vfl.mongodb.net/test?retryWrites=true&w=majority");
db = cluster["test"]
collection = db["test"]

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

path='./'
fileName='example2'
fileName_two='example3'
fileName_three='example4'
#data = {}
#data['test'] = 'test2'

token = 'Czm5aFtxepvvE4jZddlOsKXiwOzJUfl1BiFW18BfUtsUPPTkZnA663WQ13oQMdEq'
BASE_URL_ACCOUNT = 'https://canvas.sfu.ca/api/v1/accounts/10'
headers = {'Authorization': "Bearer Czm5aFtxepvvE4jZddlOsKXiwOzJUfl1BiFW18BfUtsUPPTkZnA663WQ13oQMdEq".format(token)}
auth_response_details = requests.get(BASE_URL_ACCOUNT, headers=headers)
response_details = auth_response_details.json()
json_response_details = json.dumps(response_details)
mongoImp_details = collection.insert(response_details)
#writeToJSONFile(path,fileName, response)
#request_type = "POST"
#data = {"email":"email", "name": "name"}
#api_url = "https://canvas.sfu.ca/api/v1/accounts/10/account_notifications"
#response = requests.request(request_type, api_url, data=data)

@app.route("/")
def hello():
    return jsonify(json_response_details)

if __name__ == "__main__":
    app.run()

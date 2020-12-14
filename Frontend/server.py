from flask import Flask,render_template, request, session, Response, redirect
#from database import connector
#from model import entities
import json
import time

#db = connector.Manager()
#engine = db.createEngine()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

@app.route('/search/<content>', methods = ['GET'])
def search(content):
    data = []
    with open('text.json') as file:
        text = json.load(file)
    response = {}
    i = 0
    for d in data:
        response[i] = text[d]
        i += 1
    return Response(json.dumps(response), mimetype='application/json')

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
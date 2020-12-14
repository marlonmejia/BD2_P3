import os
from flask import Flask, render_template, request, session, Response, redirect
#from database import connector
#from model import entities
from werkzeug.utils import secure_filename
import json
import face_recognition
import time

from Backend.QueryKNN_Sequential import knnSequential

#db = connector.Manager()
#engine = db.createEngine()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./img"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

@app.route('/search/<RorK>/<KNN>/<picture>', methods = ['GET'])
def search(RorK, KNN, picture):
    filename = secure_filename(picture.filename)
    picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return "Archivo Subido"

    img = face_recognition.load_image_file(picture)
    unknown_face_encodings = face_recognition.face_encodings(img)

    query = list(unknown_face_encodings[0])
    for point in unknown_face_encodings[0]:
        query.append(point)
    if KNN == 2:
        data = knnSequential(query, RorK)
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
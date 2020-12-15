import os
from flask import Flask, jsonify, render_template, request, session, Response, redirect
#from database import connector
#from model import entities
from werkzeug.utils import secure_filename
import json
import face_recognition
import time

from Backend.QueryKNN_Sequential import knnSequential
from Backend.QueryKNN_RTree import knnRtree
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


#db = connector.Manager()
#engine = db.createEngine()

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        KNN = request.form['KNN']
        RorK = request.form['RorK']
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if KNN == 'Sequential':
            if file and allowed_file(file.filename):
                img = face_recognition.load_image_file(file)
                unknown_face_encodings = face_recognition.face_encodings(img)[0]
                data = knnSequential(unknown_face_encodings, int(RorK), "Backend/")
                results = '''
                    <!doctype html>
                    <title>Buscador</title>
                    <h1>Buscador</h1>
                    <label for="cars">Busqueda KNN:</label>
                    <select name="KNN" id="KNN" form="form">
                      <option value="RTree">RTree</option>
                      <option value="Sequential">Sequential</option>
                    </select>
                    <form method="POST" enctype="multipart/form-data" id="form">
                      <input type="number" name="RorK">
                      <input type="file" name="file">
                      <input type="submit" value="Cargar">
                    </form>
                    '''
                for d in data:
                    results += '''<img src="/static/''' + d + '''" class="img-fluid" alt="Responsive image">'''
                return results
        if KNN == 'RTree':
            if file and allowed_file(file.filename):
                data = []
                img = face_recognition.load_image_file(file)
                unknown_face_encodings = face_recognition.face_encodings(img)[0]
                query = list(unknown_face_encodings)
                for point in unknown_face_encodings:
                    query.append(point)
                data = knnRtree(query, int(RorK), "Backend/")
                results = '''
                    <!doctype html>
                    <title>Buscador</title>
                    <h1>Buscador</h1>
                    <label for="cars">Busqueda KNN:</label>
                    <select name="KNN" id="KNN" form="form">
                      <option value="RTree">RTree</option>
                      <option value="Sequential">Sequential</option>
                    </select>
                    <form method="POST" enctype="multipart/form-data" id="form">
                      <input type="number" name="RorK">
                      <input type="file" name="file">
                      <input type="submit" value="Cargar">
                    </form>
                    '''
                for d in data:
                    results += '''<img src="/static/''' + d + '''" class="img-fluid" alt="Responsive image">'''
                return results

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <title>Buscador</title>
    <h1>Buscador</h1>
    <label for="cars">Busqueda KNN:</label>
    <select name="KNN" id="KNN" form="form">
      <option value="RTree">RTree</option>
      <option value="Sequential">Sequential</option>
    </select>
    <form method="POST" enctype="multipart/form-data" id="form">
      <input type="number" name="RorK">
      <input type="file" name="file">
      <input type="submit" value="Cargar">
    </form>
    '''

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

@app.route('/static/<content>')
def static_content_2(content):
    return content

@app.route('/search/<RorK>/<KNN>/<picture>', methods = ['GET'])
def search(RorK, KNN, picture):
    data = []
    path = "static/img/"+picture
    img = face_recognition.load_image_file(path)
    unknown_face_encodings = face_recognition.face_encodings(img)
    query = list(unknown_face_encodings[0])
    for point in unknown_face_encodings[0]:
        query.append(point)
    if KNN == "2":
        data = knnSequential(query, int(RorK))
    response = {}
    i = 0
    for d in data:
        response[i] = d
        i += 1
    return Response(json.dumps(response), mimetype='application/json')

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
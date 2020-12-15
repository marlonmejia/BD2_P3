from rtree import index
import face_recognition
from time import time
from os import listdir
from os.path import isfile, join
import numpy as np
import json
from flask import Flask, jsonify, request, redirect

imgdir = "LabeledFacesintheWild/"
LIMIT = 12800

def knnRtree(Query, K):
    p = index.Property()
    p.dimension = 128  # D
    idx = index.Index(properties=p)
    info = []
    Personas = listdir(imgdir)
    val = 0
    for i in Personas:
        fotos = [j for j in listdir(imgdir + i) if isfile(join(imgdir + i, j))]
        for k in fotos:
            name = k.split(".")[0]
            if isfile(imgdir + i + '/' + name + '.json'):
                with open(imgdir + i + '/' + name + '.json') as file:
                    data = json.load(file)
                path = imgdir + i + "/" + k
                print(path)
                if k != "data.json" and k != name + '.json':
                    points = data[path]
                    info.append(path)
                    for j in range(len(data[path])):
                        points.append(data[path][j])
                    idx.insert(val, points)
                    val += 1
            if (val >= LIMIT):
                break
        if (val >= LIMIT):
            break
    print("Finish")
    result = list(idx.nearest(coordinates=list(Query), num_results=K))
    Result = []
    for i in result:
        Result.append(info[i])
    return Result

img = face_recognition.load_image_file("Test/img.png")
unknown_face_encodings = face_recognition.face_encodings(img)

query = list(unknown_face_encodings[0])
for point in unknown_face_encodings[0]:
    query.append(point)

start_time = time()
print(knnRtree(query, 3))
elapsed_time = time() - start_time
print("Elapsed time: %0.10f seconds." % elapsed_time)


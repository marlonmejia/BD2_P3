from rtree import index
import face_recognition
import numpy as np
import json
from flask import Flask, jsonify, request, redirect

def knnRtree(Query, k):
    with open('data.json') as file:
        data = json.load(file)
    p = index.Property()
    p.dimension = 128  # D
    idx = index.Index(properties=p)
    result = []
    val = 0
    for i in data:
        print(i)
        points = data[i]
        for j in data[i]:
            print(j)
            points.append(j)
        print(val)
        idx.insert(val, points)
        val += 1
    result = list(idx.nearest(coordinates=list(Query), num_results=k))
    return result


img = face_recognition.load_image_file("Test/img.png")
unknown_face_encodings = face_recognition.face_encodings(img)
with open('data.json') as file:
    data = json.load(file)

query = list(unknown_face_encodings[0])
for point in unknown_face_encodings[0]:
    query.append(point)

print(knnRtree(query, 3))


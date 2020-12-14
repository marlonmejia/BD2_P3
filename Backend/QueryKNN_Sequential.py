import face_recognition
import numpy as np
from os import listdir
from os.path import isfile, join
from rtree import index
import json

imgdir = "LabeledFacesintheWild/"

def knnSequential(Query, r):
    with open('data.json') as file:
        data = json.load(file)
    result = {}
    for i in data:
        for j in range(len(Query)):
            dist = face_recognition.face_distance([data[i]], Query[j])
            if dist < r:
                result[i] = dist
    Scores_items = result.items()
    Scores_sorted = sorted(Scores_items, key=lambda coche: coche[1])
    i = 0
    Result = {}
    for doc in Scores_sorted:
        Result[doc[0]] = doc[1]
        i += 1
    return Result


#img = face_recognition.load_image_file("Test/img.png")
#unknown_face_encodings = face_recognition.face_encodings(img)


#query = list(unknown_face_encodings[0])
#for point in unknown_face_encodings[0]:
#    query.append(point)

#print(knnSequential(query, 100))

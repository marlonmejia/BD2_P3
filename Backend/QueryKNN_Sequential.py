import face_recognition
import operator
from time import time
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
        dist = face_recognition.face_distance([data[i]], Query)
        if dist <= r:
            result[i] = dist

    Result = []
    result_sorted = sorted(result.items(), key=operator.itemgetter(1))
    for name in enumerate(result_sorted):
        print(result[name[1][0]])
        Result.append(name[1][0])
    return Result


img = face_recognition.load_image_file("Test/img.png")
unknown_face_encodings = face_recognition.face_encodings(img)[0]

start_time = time()
print(knnSequential(unknown_face_encodings, 100))
elapsed_time = time() - start_time
print("Elapsed time: %0.10f seconds." % elapsed_time)

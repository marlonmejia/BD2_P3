import face_recognition
import operator
from time import time
import numpy as np
from os import listdir
from os.path import isfile, join
from rtree import index
import json

imgdir = "LabeledFacesintheWild/"
LIMIT = 6400

def knnSequential(Query, r, link = ""):
    result = {}
    Personas = listdir(link + imgdir)
    val = 0
    for i in Personas:
        fotos = [j for j in listdir(link + imgdir + i) if isfile(join(link + imgdir + i, j))]
        for k in fotos:
            name = k.split(".")[0]
            if isfile(link + imgdir + i + '/' + name + '.json'):
                with open(link + imgdir + i + '/' + name + '.json') as file:
                    data = json.load(file)
                path = imgdir + i + "/" + k
                print(path)
                if k != "data.json" and k != name + '.json':
                    dist = face_recognition.face_distance([data[path]], Query)
                    if dist <= r:
                        result[path] = dist
                    val += 1
            if (val >= LIMIT):
                break
        if (val >= LIMIT):
            break
    Result = []
    result_sorted = sorted(result.items(), key=operator.itemgetter(1))
    for name in enumerate(result_sorted):
        print(result[name[1][0]])
        Result.append(name[1][0])
    return Result


#img = face_recognition.load_image_file("Test/img.png")
#unknown_face_encodings = face_recognition.face_encodings(img)[0]

#start_time = time()
#print(knnSequential(unknown_face_encodings, 100))
#elapsed_time = time() - start_time
#print("Elapsed time: %0.10f seconds." % elapsed_time)

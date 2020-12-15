import face_recognition
import numpy as np
from os import listdir
from os.path import isfile, join
from rtree import index
import json


def getImgChar(imgdir):
    data = {}
    Personas = listdir(imgdir)

    val = 0
    for i in Personas:
        fotos = [j for j in listdir(imgdir + i) if isfile(join(imgdir+i, j))]
        for k in fotos:
            path = imgdir + i + "/" + k
            foto = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(foto)
            data[path] = list(encodings[0])
            val += 1
            with open('data.json', 'w') as file:
                json.dump(data, file)
        #if(val >= 100):
            #with open('data.json', 'w') as file:
                #json.dump(data, file)
            #return


getImgChar("LabeledFacesintheWild/")
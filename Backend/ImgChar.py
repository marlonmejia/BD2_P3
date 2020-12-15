import face_recognition
import numpy as np
from os import listdir
from os.path import isfile, join
from rtree import index
import json


def getImgChar(imgdir):
    Personas = listdir(imgdir)
    val = 0
    data = {}
    for i in Personas:
        fotos = [j for j in listdir(imgdir + i) if isfile(join(imgdir+i, j))]
        for k in fotos:
            path = imgdir + i + "/" + k
            name = k.split(".")[0]
            if k != "data.json" and k != name + '.json':
                foto = face_recognition.load_image_file(path)
                encodings = face_recognition.face_encodings(foto)
                if len(encodings) > 0:
                    data[path] = list(encodings[0])
                    with open(imgdir + i + '/' + name + '.json', 'w') as file:
                        json.dump(data, file)
                    print(val)
                    val += 1
                    data.clear()
        if(val >= 12800):
            return


getImgChar("LabeledFacesintheWild/")
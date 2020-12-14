import face_recognition
import numpy as np
from os import listdir
from os.path import isfile, join
from rtree import index


def getImgChar(imgdir):
    vectors = []
    Personas = listdir(imgdir)

    p = index.Property()
    p.dimension = 128  # D
    p.buffering_capacity = 3  # M
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    idx = index.Index('face_recognition_index', properties=p)

    val = 0
    for i in Personas:
        fotos = [j for j in listdir(imgdir + i) if isfile(join(imgdir+i, j))]
        for k in fotos:
            foto = face_recognition.load_image_file(imgdir + i + "/" + k)
            encodings = face_recognition.face_encodings(foto)

            for e in encodings:
                points = list(e)
                for point in e:
                    points.append(point)
                idx.insert(val, points)
                val += 1
        if(val >= 100):
            return


getImgChar("LabeledFacesintheWild/")
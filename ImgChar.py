import face_recognition
from os import listdir
from os.path import isfile, join
from rtree import index


def getImgChar(imgdir):
    vectors = []
    Personas = listdir(imgdir)
    for i in Personas:
        fotos = [j for j in listdir(imgdir + i) if isfile(join(imgdir+i, j))]
        for k in fotos:
            foto = face_recognition.load_image_file(imgdir + i+ "/" + k)
            encoding = face_recognition.face_encodings(foto)
            par = (i, encoding)
            vectors.append(par)
            p = index.Property()
            p.dimension = 128 #D
            p.buffering_capacity = 3 #M
            p.dat_extension = 'data'
            p.idx_extension = 'index'
            idx = index.Index('face_recognition_index',properties=p)
            val = 0
            if len(encoding) > 0:
                for i in range(len(encoding)):
                    idx.insert(val,i)
                    val = val + 1
    return vectors



getImgChar("LabeledFacesintheWild/")
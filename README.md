# BD2_P3

## Integrantes:
- Luis Cordero
- Victor Ascuña
- Marlon Mejia

## Base de Datos Multimedia

Para este proyecto se tuvo como objetivo aplicar los conocimientos adquiridos con respecto a las bases de datos multimedia e indexación. Para la demostración y testeo del proyecto se empleó un repositorio publico de imagenes llamada "Labeled Faces in the Wild". Estas imagenes son fotos reales de gente famosa o importante. Así mismo que se emplea gran cantidad de imagenes para una mejor prueba de desempeño.

## Frontend
Para el frontend se utlizo un codigo de html por programado en pythony utilizado como retorno. Dicho codigo continen lo ensencial para realizar las busquedas nesesarias. Pidiendo el tipo de busqueda a realizar; si es secuencial pide el rango, si es rtree pide el k y obviamente la imagen a comparar.
Además las busquedas retornan una lista de imagenes ordenadas segun la distancia, en caso de la busqueda secuencial, y las imagenes ordenadas segun una cola de prioridad, en caso sea busqueda rtree.

```html
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
```

![Alt text](/../main/README_IMGS/img.png?raw=true "Optional Title")
![Alt text](/../main/README_IMGS/img_1.png?raw=true "Optional Title")
![Alt text](/../main/README_IMGS/img_2.png?raw=true "Optional Title")

[Codigo](https://github.com/marlonmejia/BD2_P3/blob/main/server.py)
## Backend

### Extracción de caracteristicas
Para extraer las características de las imagenes se empleó el encoding que brindaba la libreria face-recognition. Este encoding nos retornaba un vector de 128 dimensiones por imagen, y es el que empleamos para realizar la indexación y la búsqueda. Así mismo cada vector está emparejado con el nombre de la persona a la cual pertenece cada 

### Indexación
En la parte de Indexación se utilizo rtree al momento de generar la consulta en python. Para esto se configuro el número de dimensiones a trabajar de 2 a 128 debido a face recognition. Además de insertar las caracateristicas de cada imagen extraida con anterioridad. 

```python
p = index.Property()
p.dimension = 128  # D
idx = index.Index(properties=p)
info = []
val = 0
```
```python
points = data[path]
info.append(path)
for j in range(len(data[path])):
    points.append(data[path][j])
idx.insert(val, points)
val += 1
```

[Codigo](https://github.com/marlonmejia/BD2_P3/blob/main/Backend/QueryKNN_RTree.py)

### Búsqueda
Para el tema de las consultas utilizamos KNN-RTree con cola de prioridad y KNN-Secuencial a partir de un rango. En ambos casos recibimos un valor numerico acompañado de los vectores caracteristicos de la imagen. Estos vectores caracteristicos se extraen de la imagen cargada por el usuario.

```python
# KNN-Sequential
if file and allowed_file(file.filename):
    # Extracción de vectores caracteristicos
    img = face_recognition.load_image_file(file)
    unknown_face_encodings = face_recognition.face_encodings(img)[0]
    # Llamada a la función
    data = knnSequential(unknown_face_encodings, int(RorK))
```


```python
#KNN-RTree
if file and allowed_file(file.filename):
    # Extracción de vectores caracteristicos
    img = face_recognition.load_image_file(file)
    unknown_face_encodings = face_recognition.face_encodings(img)[0]
    # Duplicación de los vectores caracteristicos
    query = list(unknown_face_encodings)
    for point in unknown_face_encodings:
        query.append(point)
    # Llamada a la función
    data = knnRtree(query, int(RorK))
```

Luego de sacar los vectores caracteristicos se realiza la función de busqueda la cual por medio del archivos ```.json``` obtiene los vectores caracteristicos de un grupo o de todos las imagenes de galeria. Con ello podemos crear el rtree y utilizar la busqueda de KNN-RTree. Esta función utiliza ```idx.nearest()``` para obtener la lista de imagenes obtenidas por medio de la busqueda KNN-RTree.


```python
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
```

[Codigo](https://github.com/marlonmejia/BD2_P3/blob/main/Backend/QueryKNN_RTree.py)

Asu vez con los mismos vectores caracteristicos se realiza la busqueda secuencial la cual utiliza la función ```face_recognition.face_distance()``` para hallar la distancia euclidiana entre ambos vectores.


```python
def knnSequential(Query, r):
    result = {}
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
```

[Codigo](https://github.com/marlonmejia/BD2_P3/blob/main/Backend/QueryKNN_Sequential.py)

### Resultados
Para las pruebas intentaremos aplicar con una cierta cantidad de imagenes, siendo N el tamaño de la coleccion de imagenes a usar en la prueba.

| Tiempo  | KNN - RTree  | KNN - Secuencial  |
|---|---|---|
| N = 100  | 0.1132431030  | 0.0147001743  |
| N = 200  | 0.2450451851  | 0.0341603756  |
| N = 400  |   |   |
| N = 800  |   |   |
| N = 1600  |   |   |
| N = 3200  |   |   |
| N = 6400  |   |   |
| N = 12800  | 29.6217381954  | 4.3440961838  |

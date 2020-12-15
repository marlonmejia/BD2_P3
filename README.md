# BD2_P3

## Integrantes:
- Luis Cordero
- Victor Ascuña
- Marlon Mejia

## Base de Datos Multimedia

Para este proyecto se tuvo como objetivo aplicar los conocimientos adquiridos con respecto a la

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




[Codigo](https://github.com/marlonmejia/BD2_P3/blob/main/server.py)
## Backend

### Extracción de caracteristicas
Para extraer las características de las imagenes se empleó el encoding que brindaba la libreria face-recognition. Este encoding nos retornaba un vector de 128 dimensiones por imagen, y es el que empleamos para realizar la indexación y la búsqueda. Así mismo cada vector está emparejado con el nombre de la persona a la cual pertenece cada 

![Alt text](/../main/README_IMGS/img.png?raw=true "Optional Title")
![Alt text](/../main/README_IMGS/img_1.png?raw=true "Optional Title")
![Alt text](/../main/README_IMGS/img_2.png?raw=true "Optional Title")

### Indexación


### Búsqueda



### Resultados
Para las pruebas intentaremos aplicar con una cierta cantidad de imagenes, siendo N el tamaño de la coleccion de imagenes a usar en la prueba.

| Tiempo  | KNN - RTree  | KNN - Secuencial  |
|---|---|---|
| N = 100  |   |   |
| N = 200  |   |   |
| N = 400  |   |   |
| N = 800  |   |   |
| N = 1600  |   |   |
| N = 3200  |   |   |
| N = 6400  |   |   |
| N = 12800  |   |   |

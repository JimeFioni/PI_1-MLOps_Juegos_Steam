![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
![Numpy](https://img.shields.io/badge/-Numpy-333333?style=flat&logo=numpy)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-333333?style=flat&logo=matplotlib)
![Seaborn](https://img.shields.io/badge/-Seaborn-333333?style=flat&logo=seaborn)
![Scikitlearn](https://img.shields.io/badge/-Scikitlearn-333333?style=flat&logo=scikitlearn)
![FastAPI](https://img.shields.io/badge/-FastAPI-333333?style=flat&logo=fastapi)
![TextBlob](https://img.shields.io/badge/-TextBlob-333333?style=flat&logo=textblob)
![Render](https://img.shields.io/badge/-Render-333333?style=flat&logo=render)
## PI_1-MLOps Juegos Steam - Modelo de recomendación

Repositorio para Proyecto Individual 1 de Machine Learning en bootcamp Henry

### Descripción del proyecto:

El objetivo del proyecto es simular el rol de un MLOps Engineer, la combinación de un Data Engineer y Data Scientist, que trabaja para la plataforma de juegos Steam.
El problema de negocio que se plantea es crear un `Producto Minimo Viable (MVP)`, que contenga una `API`deployada y con un modelo de `Machine Learning` que contenga un análisis de sentimientos a partir de los comentarios de los usuarios y un sistema de recomendación de videojuegos para la plataforma. 

### Datos:

Para desarrollar el proyecto se ha basado en tres archivos de tipo JSON GZIP:

+ **output_steam_games.json** es un dataframe que contiene información sobre los juegos; como nombre del juego, editor, dessarrollador, precios, tags.

+ **australian_users_items.json** es un dataframe que contiene información sobre cada juego que utilizan los usuarios, y el tiempo que cada usuario jugo.

+ **autralian_users_reviews.json** es un dataframe que contiene los comentarios que los usuarios realizaron sobre los juegos que utilizan , recomendaciones o no de ese juego; además de datos como url y user_id.

Los detalles de los [Dataset](/images/diccionario_games.JPG) 


### Tareas desarrolladas:

#### ETL Extracción, Transformación y Carga

En este punto se generaron los siguientes Notebooks [ETL_steam](/ETL_steam_games.ipynb),[ETL_reviews](/ETL_user_reviews.ipynb) y [ETL_items](/ETL_user_items.ipynb).

En esta fase del proyecto se realiza la extracción de datos desde los dataframes iniciales, a fin de familiarizarse con ellos y comenzar con la etapa de `limpieza de datos`; es decir extraer todo aquello que no nos permita el correcto entedimiento y lectura del archivo a fin de lograr los objetivos.
Terminada la limpieza se generan los dataset para la siguiente fase. Para este caso se comprimieron a formato `parquet`

#### Feature engineering

En esta fase del proyecto se realiza el análisis de sentimientos, utilizando la librería `textBlob`aplicada a una de las columnas donde se encuantran los comentarios de los usuarios, en el dataset `user_reviews`. Lo que da como resultado una nueva columna donde se clasifican los sentimiemtos. La librería TextBlob es parte de una biblioteca de procesamiento de lenguje natural (NLP); la que toma un comentario de un user calcula la polaridad del sentimiento y luego la clasifica como negativa, neutral o positiva .

Además de la utilización de esta metodología, en esta fase, se preparan los datasets necesarios para el tratamiento de cada función específica Logrando la optimización y mejora de los tiempos,  del funcionamiento del servicio de la nube para deployar la API y resolver las consultas.

En notebook resultante [Feature_engineering](/F_eng_y_API.ipynb)

#### Análisis Exploratorio de los Datos

En esta fase del proyecto se realiza el análisis de los tres dataset luego del ETL, para obtener una mejor visualización de cada variable categórica y numérica. A fin de identificar cuáles son las variables necesarias para el modelo de recomendación objeto final del Machine Learning.

En notebook resultante [Analisis exploratorio](/EDA.ipynb)

### Desarrollo de API

Para el desarrolo de la API se utiliza el framework FastAPI, creando las siguientes funciones:

* **`userdata`**: Esta función tiene por parámentro 'user_id' y devulve la cantidad de dinero gastado por el usuario, el porcentaje de recomendaciones que realizó sobre la cantidad de reviews que se analizan y la cantidad de items que consume el mismo.

* **`countreviews`**: En esta función se ingresan dos fechas entre las que se quiere hacer una consulta y devuelve la cantidad de usuarios que realizaron reviews entre dichas fechas y el porcentaje de las recomendaciones positivas (True) que los mismos hicieron.

* **`genre`**: Esta función recibe como parámetro un género de videojuego y devuelve el puesto en el que se encuentra dicho género sobre un ranking de los mismos analizando la cantidad de horas jugadas para cada uno.

* **`userforgenre`**: Esta función recibe como parámetro el género de un videojuego y devuelve el top 5 de los usuarios con más horas de juego en el género ingresado, indicando el id del usuario y el url de su perfil.

* **`developer`**: Esta función recibe como parámetro 'developer', que es la empresa desarrolladora del juego, y devuelve la cantidad de items que desarrolla dicha empresa y el porcentaje de contenido Free por año por sobre el total que desarrolla.

* **`sentiment_analysis`**: Esta función recibe como parámetro el año de lanzamiento de un juego y según ese año devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento, como Negativo, Neutral y Positivo.

* **`recomendacion_juego`**: Esta función recibe como parámetro el nombre de un juego (id) y devuelve una lista con 5 juegos recomendados similares al ingresado.

> *NOTA: recomendacion_juego se agrega a la API, pero sólo recomendacion_juego en el notebook de modelado es la correcta con la función y los archivos de entrada; ya que no se pudo deployar en Render dado que el conjunto de datos que requiere para hacer la predicción excedía la capacidad de almacenamiento disponible. Por lo tanto, para utilizarla se puede ejecutar la API en local.*

### Modelamiento (Machine Learning Model Development)

En esta fase del proyecto se toman los dataset logrados en la etapa de Feature engineering. A partir del data `steam_games`, con las columnas que traen los generos de videojuegos, los títulos e identificación. 

* **`recomendacion_juego`**: Esta función recibe como parametro el "id" de un titulo de juego y devuelve una lista con 5 juegos recomendacos similares al ingresado tomando como base de similitus el genero. Realizando una comparación  `item_item`

El desarrollo de las funciones de consultas generales y desarrollo de código para el modelo de recomendación se puede ver en el Notebook [Modelado](/Modelado%20ML.ipynb). 

### FastAPI

El código para generar la API se encuentra en el archivo [Main](/main.py). En caso de querer ejecutar la API desde localHost se deben seguir los siguientes pasos:

- Clonar el proyecto haciendo `git clone https://github.com/JimeFioni/PI_1-MLOps_Juegos_Steam.git`.
- Preparación del entorno de trabajo en Visual Studio Code:
    * Crear entorno `python -m venv env`
    * Ingresar al entorno haciendo `env\Scripts\activate`
    * Instalar dependencias con `pip install -r requirements.txt`
- Ejecutar el archivo `main.py` desde consola activando uvicorn. Para ello, hacer `uvicorn main:app --reload`
- Hacer Ctrl + clic sobre la dirección `http://XXX.X.X.X:XXXX` (se muestra en la consola).
- Una vez en el navegador, agregar `/docs` para acceder a ReDoc.
- En cada una de las funciones hacer clic en *Try it out* y luego introducir el dato que requiera o utilizar los ejemplos por defecto. Finalmente Ejecutar y observar la respuesta.

### Deploy 

Para el deploy de la API se seleccionó la plataforma Render que es una nube unificada para crear y ejecutar aplicaciones y sitios web, permitiendo el desplegue automnático desde GitHub. 

* Se generó un nuevo servicio en `render.com`, conectando a este repositorio

* Se genera el link donde queda corriendo https://pi1-steamgames-deploy-jimefioni.onrender.com 

### Video

La explicación y demostración del funcionamiento de la API en el [Video]

### Conclusiones 

El proyecto se ha llevado a cabo, utilizando los conocimientos obtenidos durante el cursado de la carrera Data Science en HENRY.
Puede decirse que las tareas comprendidas aquí son las habituales del un Data Engineer y Data Scientist. 
Se logro el objetivo de un Producto Minimo MPV, con una API y su deploy en un servicio web. Si bien, se el objetivo se cumple; debe decirse que por motivos de almacenamiento, en muchos casos se realizan los procesos básicos, por lo que las funciones utilizadas pudieran optimizarse en sus resultados más aún.








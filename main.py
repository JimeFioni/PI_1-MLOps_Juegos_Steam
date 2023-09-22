"""
AQUI SE ENCUENTRAN LAS FUNCIONES CREADAS PARA EL PROYECTO INTEGRADOR 1 
MLOPS - STEAM GAMES - 

FUNCIONES PARA ALIMENTAR LA API
"""

#librerías
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity

#instanciar la aplicación

app = FastAPI()


#dataframes que se utilizan en las funciones de la API
user_reviews = pd.read_parquet("data/user_review.parquet")
cant_items = pd.read_parquet("data/cant_items.parquet")
recommend = pd.read_parquet("data/recommend.parquet")
rank_genre = pd.read_parquet("data/rank_genre.parquet")
user_hours = pd.read_parquet("data/user_hours.parquet")
devs = pd.read_parquet("data/devs.parquet")
sentimiento_analysis = pd.read_parquet("data/sentimiento_analysis.parquet")
modelo_item= pd.read_parquet("data/modelo_item.parquet")


@app.get("/", response_class=HTMLResponse)
async def incio ():
    principal= """
    <!DOCTYPE html>
    <html>
        <head>
            <title>API Steam</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>API de consultas sobre juegos de la plataforma Steam</h1>
            <p>Bienvenido a la API de Steam donde se pueden hacer diferentes consultas sobre la plataforma de videojuegos.</p>
            <p>INSTRUCCIONES:</p>
            <p>Escriba <span style="background-color: lightgray;">/docs</span> a continuación de la URL actual de esta página para interactuar con la API</p>
            <p>Consulte en el siguiente enlace:<a href="http://127.0.0.1:8000/docs#/">{{FastAPI}}</a></p>
            <p> El desarrollo de este proyecto esta en <a href="https://github.com/JimeFioni/PI_1-MLOps_Juegos_Steam"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-black?style=flat-square&logo=github"></a></p>
            <p>María Jimena Fioni - 2023 -</p>
        </body>
    </html>

        """    
    return principal




#Primera función
@app.get( "/userdata/{user_id}", name = "USERDATA")
async def userdata(user_id : str):
    """
    La siguiente función retorna información sobre el usuario que se le pasa como argumento

    Parametro: 
    
            user_id(str) : ID del Usuario a consultar.
    Retorna:
    
            user (dict): Información de un usuario ,
            -cantidad de dinero gastado (int): Dinero gastado por usuario
            -Porcentaje de recomendación usuario (float): Reviews realizadas por el usuario con respecto a la cantidad de 
            reviews por usuario
            -cantidad de items (int):cantidad de juegos consumidos por usuario 
    
    Ejemplo:
    
            user_id: js41637
    """

    #igualo el user_id al user_id del dataframe con los datos de los reviews 
    user= user_reviews[user_reviews["user_id"]== user_id]
    #sumo la columna price del dataframe cant_items par conocer el gasto por usuario
    gasto = cant_items[cant_items["user_id"]== user_id]["price"].sum()
    
    #cantidad de recomendaciones del usuario ingresado
    rec_user= recommend[recommend["user_id"]== user_id]["recommend"].sum()
    #cantidad de recomendaciones totales por usuario
    total_rec= len(user_reviews["user_id"].unique())
    porcentaje=(rec_user/total_rec)*100
    
    #cuento la cantidad de jueagos que utilizo el usuario 
    count= cant_items[cant_items["user_id"]== user_id]["items_count"].iloc[0]
    return{
        "Cantidad de dinero gastado": int (gasto),
        "Porcentaje de recomendación usuario": round(float(porcentaje), 3),
        "Cantidad de items": int(count)
    }
    
    




#Segunda función
@app.get("/countreviews/{f_inicio}/{f_final}", name = "COUNTREVIEWS")
async def countreviews(f_inicio,f_final):
    """
    La siguiente función retorna la cantidad de usuarios que realizaron reviews y el porcentaje de reviews de estos con respecto al total de usuarios en un rango de fechas

    Parametros:
    
            -f_inicio(str/datetime): Fecha de inicio del rango a evaluar 
            -f_final(str/datetime): Fecha final del rango a evaluar 
    Retorna:
    
            -Cantidad de usuarios: con reseñas dentro de ese período de tiempo
            -Porcentaje de reviews entre fechas : del usuario con respecto al total en el período
    Ejemplo:
    
            f_inicio = 2011-11-25
            f_final = 2011-12-18
    """

    #convierte las fechas a objetos datetime en el caso de que no lo estén
    #f_inicio = pd.to_datetime(f_inicio)
    #f_final = pd.to_datetime (f_final)
    
    #crea el rango de fechas mediante el filtro
    rango_fechas=user_reviews[(user_reviews['posted']>=f_inicio)&(user_reviews['posted']<=f_final)]
    
    #calculo de la cantidad de usuarios que hicieron reviews entre esas fechas
    count_usu= rango_fechas["user_id"].nunique()
    
    #calculo el porcentaje de reviews en el mismo rango
    porcentaje_fechas=(rango_fechas["recommend"].sum() / len(rango_fechas))* 100
    
    return{
        "Cantidad de usuarios con reseñas" : count_usu ,
        "Porcentaje de reviews entre fechas": round(float(porcentaje_fechas), 3)
    }





#Tercera función
@app.get("/genre/{genero}", name = "GENRE")
async def genre(genero):
    """
    La siguiente función retorna el ranking en que se ubica el genero que se le ingresa de acuerdo a "playtime_forever"
    
    Parametros:
    
            - genero (str): el genero de juegos Steam que se quiera conocer el tiempo jugado
    Retorna:
    
            - orden: La ubicación dentro de ranking de acuerdo a la columna "playtime_forever"
    Ejemplo:
    
            -genero: Action
    """ 
    #filtro el dataframe "rank_genre" para quesu columna "genres" sea igual a el dato que se ingresa
    # a partir de esto se selecciona la columna "ranking" del conjunto resultante y se bloquea para obtener el valor
    orden= rank_genre[rank_genre["genres"]== genero]["ranking"].iloc[0]
    return {
        "El género": genero, 
        "se ubica en el raking de PlayTimeForever": int(orden)
    }





# Cuarta función
@app.get("/userforgenre/{genre}", name = "USERFORGENRE")
async def userforgenre (genero):
    """
    La siguiente función retorna el TOP 5 de usuarios junto a su información, con mayor horas de juego en el genero que se le indica
    
    Parametros:
    
            -genero (str): El genero de juego Steam del que se necesita conocer el TOP 5 de usuarios
    Retorna:
    
            -top_5_users(list) : Lista ordenada por horas de juego "playtime_forever", en forma descendente, conteniendo los nombres de usuario y dirección url
    Ejemplo:
    
            -genero: RPG
    """

    #se filtra el dataframe con la columna "genres" y se la iguala con el dato ingresado
    genre_data= user_hours[user_hours["genres"]== genero]

    #extrae los primeros 5 
    top_5_users= genre_data.head(5)
    top_5= top_5_users.to_dict(orient="records")
    return top_5






#Quinta función
@app.get("/developer/{desarrollador}", name = "DEVELOPER")
async def developer(desarrollador):
    """
    La siguiente función retorna la cantidad y porcentaje de juegos gratis por desarrollador y año

    Parametros:
    
            -desarrollador (str): El desarrollador del juego Steam que se ingresa 
    Retorna: 
    
            -Año: año en que se da el estreno del juego 
            -Cantidad de items por año: cantidad de juegos publicados por el desarrollador en el año 
            -Porcentaje de juegos free: porcentaje de juegos gratis con respecto a los publicados en ese año
    Ejemplo:
    
            -Poolians.com
    """
    
    #Se filtra el dataframe devs para igualarlo al dato que se ingresa
    data= devs[devs["developer"]== desarrollador]
    
    #Se agrupa por año para contar los items por año
    cantidad = data.groupby("release_anio")["item_id"].count()
    #Se agrupa por price para encontrar la cantidad free
    free_anio= data[data["price"]== 0.0].groupby("release_anio")["item_id"].count()
    porcentaje_gratis= (free_anio/cantidad*100).fillna(0).astype(int)
    
    #se crea una salida como dataframe
    tabla= pd.DataFrame({
        "Año": cantidad.index, #indice
        "Cantidad de items por año" : cantidad.values, #valor
        "Porcentaje de juegos free" : porcentaje_gratis.values #valor
    })
    tabla= tabla.to_dict(orient="records")
    return tabla





#Sexta función
@app.get("/sentimet_analysis/{anio}", name = "SENTIMENT_ANALYSIS")
async def sentiment_analysis(anio):

    """
    La siguiente función retorna el resultado de los analisis de sentimiento por año ingresado, 
    se tiene en cuenta el año de estreno del juego.
    
    Paramentros: 
    
            - anio (int): Año de estreno del juego
    Retorna:
    
            - count_sentiment : una lista del conteo de sentimientos
    Ejemplo:
    
            -anio: 2015
    """
    #Se filtran las reviews por año y las igualo al año que se ingresa en la consulta transformandolo en string 
    reviews_por_anio= sentimiento_analysis[sentimiento_analysis["release_anio"]== str(anio)]
    
    #Se inicia una lista vacia por cada sentimiento para ir contandolos 
    Negativos = 0
    Neutral = 0
    Positivos = 0
    
    #Se itera sobre las filas de reviews_por_anio y se distibuyen los datos segun la columna "sentiment_analysis"
    for i in reviews_por_anio["sentiment_analisis"]:
        if i == 0:
            Negativos += 1
        elif i == 1:
            Neutral += 1 
        elif i == 2:
            Positivos += 1

    count_sentiment ={"Negative": Negativos , "Neutral" : Neutral, "Positive": Positivos}
    
    return count_sentiment




#Modelo de recomendacion item_item
@app.get("/recomendacion_juego/{id}", name= "RECOMENDACION_JUEGO")
async def recomendacion_juego(id):
    
    """La siguiente funcion genera una lista de 5 juegos similares a un juego dado (id)
    Parametros:
        -id (int): El id del juego para el que se desean encontrar juegos similares

    Returna:
        -dict Un diccionario con 5 juegos similares 
    """
    id = int(id)
    # Filtrar el juego e igualarlo a  su ID
    juego_seleccionado = modelo_item[modelo_item['id'] == id]
    # devolver error en caso de vacio
    if juego_seleccionado.empty:
        return "El juego con el ID especificado no existe en la base de datos."
    
    # Calcular la matriz de similitud coseno
    similitudes = cosine_similarity(modelo_item.iloc[:,3:])
    
    # Calcula la similitud del juego que se ingresa con otros juegos del dataframe
    similarity_scores = similitudes[modelo_item[modelo_item['id'] == id].index[0]]
    
    # Calcula los índices de los juegos más similares (excluyendo el juego de entrada)
    indices_juegos_similares = similarity_scores.argsort()[::-1][1:6]
    
    # Obtener los nombres de los juegos 5 recomendados
    juegos_recomendados = modelo_item.iloc[indices_juegos_similares]['app_name']
    juegos_recomendados=juegos_recomendados.to_dict(orient="records")
    
    return juegos_recomendados
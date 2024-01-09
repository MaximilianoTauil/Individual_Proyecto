"""
Introducción:

Este archivo contiene funciones con una breve explicación de los parámetros que reciben y lo que devuelven. Los archivos se encuentran en formato Parquet serán pasados a un DataFrame para su utilización.

"""
# Importación de librerias.
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Se realiza la carga de los archivos parquet en DataFrames para su utilización.

data_playtime = pd.read_parquet('Data_parquet/data_playtime.parquet')
data_recommend = pd.read_parquet('Data_parquet/data_recommend.parquet')
data_sentiment = pd.read_parquet('Data_parquet/data_sentiment.parquet')
data_user_genre = pd.read_parquet('Data_parquet/data_user_genre.parquet')
data_users = pd.read_parquet('Data_parquet/data_users.parquet')
data_similar_cosine = pd.read_parquet('Data_parquet/data_similar_cosine.parquet')


@app.get("/PlayTimeGenre")
def PlayTimeGenre (genero:str):
    """
    Devuelve el año con más horas jugadas para dicho género

    Parámetros: 
        Género (str): El género del videojuego 
    
    """
    data_play = data_playtime[data_playtime['genres'] == genero]
    if data_play.empty:
        return f"No hay datos para el género {genero}"
    data_play = data_play.sort_values(by='playtime_forever',ascending=False).head(1)
    date = data_play['release_date'].values[0]
    feedback = (f'Año de lanzamiento con más horas jugadas para Género {genero}: {date}')
    return feedback



@app.get("/UserForGenre")
def UserForGenre(genero:str):

    """
    Devuelve el usuario que acumula más horas jugadas para un género dado
    y una lista de acumulación de horas jugadas por año.

    Parámetros: 
        Género (str): El género del videojuego 
    
    """

    data_genre = data_user_genre[data_user_genre['genres'] == genero]
    if data_genre.empty:
        return f"No hay datos para el género {genero}"
    data_usuario = data_genre.sort_values(by='playtime_forever',ascending=False).iloc[0]
    hours = data_usuario.at['playtime_forever']
    data_user =data_usuario.values[0]
    año = data_usuario.at['release_date']
    horas_anuales_usuario = data_genre.groupby('release_date')['playtime_forever'].sum().reset_index()
    horas_anuales = horas_anuales_usuario.to_dict(orient='records')
    write = (f'Usuario con más horas jugadas para el género {genero} es: {data_user}, en el año {año}: {hours} jugadas, además tenemos las horas jugadas por año del usuario {data_user}: {horas_anuales}')
    return write
            
@app.get("/UsersRecommend")
def UsersRecommend(año:int):

    """
    Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado.

    Parámetros: 
        Año (int): El año del que se utilice en la consulta
    
    """

    datarecommend = data_recommend[data_recommend['posted'] == año]
    if datarecommend.empty:
        return f"No hay datos para el año {año}"
    top3_games = datarecommend.sort_values(by= 'recommend',ascending= False).iloc[0:3]
    names = top3_games['app_name'].tolist()
    año = top3_games['posted'].tolist()
    write = f'Puesto 1:{names[0]} , Puesto 2:{names[1]} , Puesto 3:{names[2]}'
    return write

@app.get("/UsersWorstDeveloper")
def UsersWorstDeveloper(año:int):

    """
    Muestra el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios
    para el año dado

    Parámetros:
        Año (int): Año del que se utilice en la consulta
    
    """

    dfworst = data_users[(data_users['posted'] == año)]

    if dfworst.empty:
        return f"No hay datos para el año {año}"

    count_worst_dev = dfworst['developer'].value_counts()

    top_3_worst = count_worst_dev.head(3)

    top_3 = []

    for position,(developer,_) in enumerate(top_3_worst.items()):
        top_3.append({f'Puesto {position+1}:':developer})

    return top_3

@app.get("/sentiment_analysis")
def sentiment_analysis(desarrolladora:str ):

    """
    Devuelve un diccionario con el nombre de la desarrolladora y una lista con la 
    cantidad de registros de reseñas de usuarios (negativos, neutros y positivos)

    Parámetros:
        Developer (str): Desarrollador del que se quiere saber las reseñas
    """

    developer2= data_sentiment.loc[desarrolladora,[0,1,2]]
    if developer2.empty:
        return f"No se encontraron registros para la desarrolladora '{desarrolladora}'"
    developer2_list = developer2.to_list()
    write = {desarrolladora:developer2_list}
    return write


@app.get("/recomendacion_juego")
def Recomendacion_juego(id_juego:str):

    """
    Devuelve el nombre de los 5 juegos más similares al que se ingreso por parámetro.

    Parámetros:
        id_juego: Nombre del juego del cual se quiere ver los similares
    """
    if id_juego not in data_similar_cosine.columns:
        return {"message": f'El juego {id_juego} no esta disponible.'}
    orden = data_similar_cosine.sort_values(by=id_juego,ascending=False).index[1:6]
    
    similar_games = []

    for nro, game in enumerate(orden,start=1):
        similar_games.append(f'Nro {nro}: {game}')
    return {"message": f'Los 5 juegos más parecidos a {id_juego} son: {similar_games}'}
from fastapi import FastAPI
import pandas as pd
import pyarrow.parquet as pq

app = FastAPI()

#http://127.0.0.1:8000


# Se realiza la carga de los archivos parquet en DataFrames para su utilización.

data_playtime = pd.read_parquet('Data_parquet/data_playtime.parquet')
data_recommend = pd.read_parquet('Data_parquet/data_recommend.parquet')
data_sentiment = pd.read_parquet('Data_parquet/data_sentiment.parquet')
data_user_genre = pd.read_parquet('Data_parquet/data_user_genre.parquet')
data_users = pd.read_parquet('Data_parquet/data_users.parquet')



@app.get("/PlayTimeGenre")
def PlayTimeGenre (genero:str):
    data_play = data_playtime[data_playtime['genres'] == genero]
    data_play = data_play.sort_values(by='playtime_forever',ascending=False).head(1)
    date = data_play['release_date'].values[0]
    feedback = (f'Año de lanzamiento con más horas jugadas para Género {genero}: {date}')
    return feedback



@app.get("/UserForGenre")
def UserForGenre(genero:str):

    data_genre = data_user_genre[data_user_genre['genres'] == genero]
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
    datarecommend = data_recommend[data_recommend['posted'] == año]
    top3_games = datarecommend.sort_values(by= 'recommend',ascending= False).iloc[0:3]
    names = top3_games['app_name'].tolist()
    año = top3_games['posted'].tolist()
    write = f'Puesto 1:{names[0]} , Puesto 2:{names[1]} , Puesto 3:{names[2]}'
    return write

@app.get("/UsersWorstDeveloper")
def UsersWorstDeveloper(año:int):

    dfworst = data_users[(data_users['posted'] == año)]

    count_worst_dev = dfworst['developer'].value_counts()

    top_3_worst = count_worst_dev.head(3)

    top_3 = []

    for position,(developer,_) in enumerate(top_3_worst.items()):
        top_3.append({f'Puesto {position+1}:':developer})

    return top_3

@app.get("/sentiment_analysis")
def sentiment_analysis(desarrolladora:str ):
    developer2= data_sentiment.loc[desarrolladora,[0,1,2]].to_list()
    write = {desarrolladora:developer2}
    return write

from textblob import TextBlob as txb
import pandas as pd
import re
import json
import ast

def analizar_datos(df):
    


    resumen_dict = {"Nombre": [], "Tipos de Datos Únicos": [], "% de Valores No Nulos": [], "% de Valores Nulos": [], "Cantidad de Valores Nulos": []}

    for columna in df.columns:
        porcentaje_no_nulos = (df[columna].count() / len(df)) * 100
        resumen_dict["Nombre"].append(columna)
        resumen_dict["Tipos de Datos Únicos"].append(df[columna].apply(type).unique())
        resumen_dict["% de Valores No Nulos"].append(round(porcentaje_no_nulos, 2))
        resumen_dict["% de Valores Nulos"].append(round(100 - porcentaje_no_nulos, 2))
        resumen_dict["Cantidad de Valores Nulos"].append(df[columna].isnull().sum())

    resumen_dataframe = pd.DataFrame(resumen_dict)
        
    return resumen_dataframe


def extraccion_anio(col):

    match = re.search(r'\b\d{4}\b', col)
    if match:
        return match.group(0)
    else:
        return None


def extraccion_anio_wstring(col):
    division = col.split('-')
    if len(division)>2 and division[0].isdigit():
        return division[0]
    else:
        return None
        
def analisis_sentimiento(col):

    item = txb(col)
    polaridad= item.sentiment.polarity
    
    if polaridad < -0.25:
        return 0
    elif polaridad > 0.25:
        return 2
    else:
        return 1
    

def cantidad_porcentaje(dataframe, columna):
    
    cantidad = dataframe.shape[0]
    cantidad_columna = dataframe[columna].value_counts()
    porcentaje_columna = round((cantidad_columna / cantidad) * 100, 2)
    
    print(f'Los valores de {columna}\n{cantidad_columna.to_string(header=False)}')
    print(f'El porcentaje de cada valor\n{porcentaje_columna.to_string(header=False)}')

def read_json(ruta):

    filas=[]
    with open(ruta,encoding='utf-8') as r:
        for lines in r.readlines():
            try: 
                datos = json.loads(lines)
                filas.append(datos)
            except json.JSONDecodeError:
                filas.append(ast.literal_eval(lines))
    print('El archivo se leyó con éxito')
    return filas            

def export_data_csv(ruta_nueva,dataframe):
    
    dataframe.to_csv(ruta_nueva,index=False,encoding='utf-8')
    print('El archivo se exportó con éxito')
    
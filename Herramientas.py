

import pandas as pd
import re


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
        
    
# Proyecto Indiviual I Plataforma Steam

Este proyecto trata sobre la creacion de funciones, una API y un sistema de recomendacion de videojuegos de la plataforma Steam. Ademas se plantea el objetivo de un MVP (Producto Minimo Viable) como minimo. Se desarrolla bajo el rol de MLOps Engineer.

## Planteo de proyecto

La plataforma de videojuegos Steam, se encuentra en la dificultad de disponer de datos poco consistentes y de calidad para la creación de un sistema de recomendación eficiente. Los datos actuales presentan estructuras anidadas, datos faltantes esto complica el trabajo. El objetivo principal consiste en desarrollar un sistema de recomendación que ofrezca sugerencias relevantes a los usuarios, basándose en sus preferencias individuales y las reseñas de los juegos.

## Elementos de trabajo

Se otorgan 3 datasets en formato json los cuales son:
* **australian_users_items** En este dataset se almacenan identificadores de usuario, tiempo de juego y cantidad de juegos. Además tenemos las siguientes columnas: 
    * user_id
    * items_count
    * steam_id 
    * user_url
    * items
    * playtime_forever

* **australian_user_reviews** En este dataset se almacena informacion de los usuarios tales como reseñas, identificadores. Además tenemos las siguientes columnas:
    * user_id
    * user_url
    * posted
    * item_id
    * helpful
    * recommend
    * review

* **output_steam_games**  En este dataset se almacena información de los videojuegos de la plataforma. Además tenemos las siguientes columnas:
    * publisher
    * genres
    * app_name
    * title
    * url
    * release_date
    * tags
    * reviews_url
    * specs
    * price
    * early_access
    * item_id
    * developer

Si quiere revisar lo que contiene cada columna, haga clic [aquí](./Notebooks/Diccionario.ipynb) para acceder al diccionario de datos para verlo.
A lo largo del trabajo estas columnas iran mutando o desapareciendo según las necesidades planteadas.

## Transformaciones y feature Engineering

Las transformaciones en los conjuntos de datos consistieron en desanidarlos, ya que estaban en diccionarios de listas o en listas de diccionarios. Luego, se procedió a ver el tratamiento de los datos nulos o faltantes, los tipos de datos, ya que en una columna teníamos dos tipos de datos, eliminar columnas innecesarias y algunos outliers (valores fuera del rango).


El feature engineering consistía en hacer un análisis de sentimiento sobre las reseñas de los juegos hechas por los clientes o jugadores. El mismo se realizó con una librería de procesamiento de lenguaje natural llamada [**TextBlob**](https://textblob.readthedocs.io/en/dev/), con la cual se llevó a cabo un análisis sobre todos los comentarios. A partir de ello y según la polaridad del comentario (la polaridad es un valor que se asigna entre -1 y 1), se tomaron decisiones o se generaron características adicionales.
Se clasificaron los comentarios en tres valores posibles: 

* Negativo = 0
* Neutro = 1
* Positivo = 2 

Se puede acceder a los ETL de los datasets mencionados presionando el que desee: [ETL_ITEMS](./Notebooks/ETL_user.ipynb),[ETL_REVIEWS](./Notebooks/ETL_reviews.ipynb) y [ETL_GAMES](./Notebooks/ETL_output.ipynb).

## Análisis Exploratorio de Datos (EDA)
Se realizó el Análisis Exploratorio para explorar relaciones, valores fuera de rango, valores con alta carga sobre un mismo valor. Se hicieron gráficos y, además, se verificaron los tipos de datos correctos para su posterior utilización. Para acceder a el haz click [aquí](./Notebooks/EDA.ipynb).

Tanto para el EDA y los ETL, tambien se utilizo un modulo propio que esta disponible [aquí](Herramientas.py).

## Desarrollo de API

La API se construyó con el framework de [FastAPI](https://fastapi.tiangolo.com/). Las funciones requerían de una reducción en los datos, es decir, para poder desplegarlo, se debían usar menos cantidad de registros. Por eso, se seleccionaron las columnas que eran indispensables y los registros que cumplían con los valores deseados. Por ejemplo, si teníamos que ver la cantidad de horas jugadas, se eliminaban los registros que tenían 0 horas de juego. Para ver las funciones que se llevaron a cabo haga click [aquí](main.py) y será enviado al archivo main.py el cual las contiene.

Las funciones creadas son:
* ``def PlayTimeGenre( genero : str )``: Devuelve el año con mas horas jugadas para dicho género.

* ``def UserForGenre( genero : str )``: Devuelve el  usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.

* ``def UsersRecommend( año : int )``: Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. 

* ``def UsersWorstDeveloper( año : int )``: Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado.

* ``def sentiment_analysis( desarrolladora: str )``: Devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.

* ``def recomendacion_juego( id_juego )``: Ingresando el id de producto, se recibe una lista con los 5 juegos recomendados más similares al ingresado.

## Sistema de recomendación item-item

Se eligió la creación de un sistema de recomendación item-item. Esto significa que toma un ítem que se le ingresa y, en base a qué tan similar es ese ítem al resto, se recomiendan los 5 más similares. Para crearlo, se usó la similitud del coseno. Para que esto maneje un solo valor o puntaje de similaridad, se unificaron y ponderaron los valores de dos columnas: 'sentiment_analysis' y 'recommend'. La función de este sistema está en otro cuaderno (notebook). Para consultarlo, haga click [aquí](Notebooks/Sistema_recomendacion.ipynb).


## Deployment

El deployment (desplegamiento) en [Render](https://render.com/) se realizó para que el acceso a la API sea también por la web y que esté corriendo de manera constante. Este servicio se mantiene conectado con GitHub, así que cada cambio es guardado y ejecutado automáticamente en la nube. Para acceder, haga click [aquí](https://deploy-2-2fjj.onrender.com/docs#/).

Si se quieren revisar las bibliotecas instaladas para el proyecto, están [aquí](requirements.txt) en el archivo requirements.txt, el cual se desarrolló en un entorno virtual para que las dependencias o bibliotecas no generen conflictos con otros proyectos. Con este entorno, se utilizan solo dentro de él en la versión que se necesite.

## Video

En el siguiente [link](https://www.youtube.com/watch?v=WppkExf47AU&ab_channel=MaximilianoTauil) se encuentra el video con el resumen del proyecto.

## Conclusión

Es un proyecto muy interesante, te motiva a generar una buena limpieza de datos, a tocar la rama del machine learning, la cual es muy atractiva. Te obliga a buscar por cuenta propia y eso genera mucho valor para los próximos pasos que voy a dar, además de ver que se pueden hacer consultas desde otro lugar, no solo de forma local.



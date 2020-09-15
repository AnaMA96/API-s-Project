import os
from dotenv import load_dotenv
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from bubbly.bubbly import bubbleplot 
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode()
import plotly.express as px
import plotly 


import time


def importCsv():
    f importCsv():
    """
        Carga en la variable global temp el dataframe, generado a
        partir del fichero csv "output/temperature_per_city",
        para poder acceder desde las demás funciones y, de paso, transforma
        los grados de ºF a ºC de la columna de temperatura media.
    """
    global temp
    temp = pd.read_csv("output/temperature_per_city",encoding='latin-1', low_memory=False)
    temp["avgtemperature"] = temp['avgtempcelsius'] = (temp.avgtemperature -32)*(5/9)
    temp = temp.drop(['avgtemperature'], axis = 1)
    temp['avgtempcelsius_rounded'] = temp.avgtempcelsius.apply(lambda x: "{0:0.1f}".format(x))
    temp['avgtempcelsius_rounded'] = pd.to_numeric(temp['avgtempcelsius_rounded'])


def filterDataFrame(df, city, start_date, end_date):
    """
    Gráfico que muestra la evolución de la temperatura media de la tierra entre los años
    que se le indiquen.
    """
    plot_df = df
    if city != "":
        plot_df = plot_df[(plot_df["city"]== f"{city}")]
    plot_df['date'] = pd.to_datetime(plot_df["date"])
    plot_df = plot_df[(plot_df["date"] >= start_date) & (plot_df["date"] <= end_date)]

    return plot_df
   
def plotDataFrame(plot_df, title):
    """
    Esta función sirve para sacar un plot con la evolución de la temperatura media
    del dataframe que recibe la función.
    """
    plot_df = plot_df.set_index('date')
    plot_df = plot_df.groupby([pd.Grouper(freq = "M")]).mean()

    if title == "":
        title = "Earth"
    plt.figure(figsize = (10,8))
    plt.plot(plot_df.index, plot_df.values, marker ="o")
    plt.xticks(size =10)
    plt.ylabel("average Temperture",size = 15)
    plt.yticks(size =15)
    plt.title(f"Growth of the average Temperture ({title})",size =20)
    plt.show()   
    plt.savefig("AvgTemperature Plot")

def geocode(address):
    """
    Saca las coordenadas de una dirección que le des.
    """
    data = requests.get(f"https://geocode.xyz/{address}?json=1").json()
    return {
        "lon":float(data["longt"]),
        "lat":float(data["latt"])}

def getFromAPI(coordinates,start,end):
    """
        Esta función hace una petición a la api de meteostat,
        con las coordenadas, fecha de comienzo y de final, 
        para obtener datos sobre el tiempo,
        y devuelve el json de la respuesta.
    """
    url = f'https://api.meteostat.net/v2/point/daily?lat={coordinates["lat"]}&lon={coordinates["lon"]}&start={start}&end={end}'
    headers = {"x-api-key": "{api-key}"}
    res = requests.get(url, headers=headers)
    print(url)
    print(res)
    return res.json()

def dataFrameCallingAPI(city, start_date, end_date):
    """
        Esta función llama a geocode para obtener las coordenadas
        de la ciudad recibida, llama a getFromAPI para obtener el json 
        sobre el tiempo dentro de un rango de fechas, añade el campo
        "city" en cada entrada de los datos y lo devuelve en
        forma de dataframe.
    """
    coordinates = geocode(city)

    json = getFromAPI(coordinates, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

    data = json["data"]

    for item in data:
        item["city"] = city

    df = pd.DataFrame(data)
    df = filterDataFrame(df, city, start_date, end_date)
    return df

def avgTemp(df):
    """
        Esta función genera un dataframe escogiendo las columnas de
        temperatura media y fecha y lo devuelve.
    """
    avgTempDataFrame = df[["tavg", "date"]]
    return avgTempDataFrame

def rainChange(df):
     """
        Esta función muestra filtra por "year" el dataframe que recibe para mostrar las precipitaciones por año en un gráfico de barras.
    """
    plot_df = df.reset_index()
    plot_df["year"] = plot_df.apply(lambda row: row["date"].year, axis=1)
    plot_df = plot_df.groupby(by='year')['prcp'].sum().reset_index()
    plot_df['change'] = 0
    for i in range(1,plot_df.shape[0]):
        plot_df.loc[i,'change'] = (plot_df.loc[i,'prcp']-plot_df.loc[i-1,'prcp'])/plot_df.loc[i-1,'prcp']
    plt = px.bar(plot_df, 'year', 'change', color='change', title = 'Change in rainfall over the years :', color_continuous_scale=px.colors.sequential.Cividis)
    plotly.offline.plot(plt, filename = "Rain Change Plot")

def callingApiForYears(start, end, city):
    """
        Esta función concatena todas las respuestas de la API.
        Realiza una petición por cada año que haya entre start y end, 
        crea un dataframe con los datos, llama a filterDataFrame, para 
        filtrar los datos y devuelve el dataframe filtrado.
    """
    if city == "":
        return

    coordinates = geocode(city)

    start_year = start.year
    end_year = end.year

    data = []
    if start_year != end_year:
        json = getFromAPI(coordinates, start.strftime('%Y-%m-%d'), f"{start_year}-12-31")
        data += json["data"]

        for year in range(start_year + 1, end_year):
            time.sleep(1)
            json = getFromAPI(coordinates, f"{year}-01-01", f"{year}-12-31")
            data += json["data"]
            
        
        json = getFromAPI(coordinates, f"{end_year}-01-01", end.strftime('%Y-%m-%d'))
        data += json["data"]

    for item in data:
        item["city"] = city

    df = pd.DataFrame(data)
    df = filterDataFrame(df, city, start, end)
    return df

def maxTempByCountry(avgtemp):
    """
        Esta función filtra las entradas del dataframe global temp
        a partir de una temperatura media e imprime los países que 
        igualan o sobrepasan la temperatura recibida.
    """
    lst = set()
    temp_by_country_df = temp[temp["avgtempcelsius_rounded"] >= avgtemp]

    for country in temp_by_country_df["country"]:
        lst.add(country)

    print(f'The countries that have reached and / or exceeded the indicated temperature are:{lst}')




    
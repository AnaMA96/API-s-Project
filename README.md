# API-s-Project
![Alt Text](https://www.coe.int/documents/18550040/24135798/20200428-Online-First-regional.jpg/0ce96786-160d-ba7d-d874-b89cae70e603?t=1588625448000)

## El cambio climático. ¿Realidad o mito. Análisis de la evolución de las temperaturas a lo largo de los años desde 1995 hasta la actualidad en diferentes ciudades del mundo.

**"Global warming is the ongoing rise of the average temperature of the Earth's climate system and has been demonstrated by direct temperature measurements and by measurements of various effects of the warming - Wikipedia.So a dataset on the temperature of major cities of the world will help analyze the same."**

En este proyecto utilizo el dataset [Daily Temperature of Major Cities](https://www.kaggle.com/sudalairajkumar/daily-temperature-of-major-cities), que me ofrece información acerca de la temperatura media de las ciudades de diferentes países del mundo hasta mayo de 2020. Esa información ha sido completada con la ofrecida por la **API "Meteostat"** para poder obtener los datos de los últimos meses así como otros relativos al tiempo como las precipitaciones medias por fecha y lugar. Para armonizar los datos, la columna de temperatura media del dataset ha sido transformada de ºF a ºC.
A su vez, la API "Meteosat" se sirve de las coordenadas obtenidas por la **API "Geocode"** al hacer la llamada con el nombre de una ciudad concreta.

El dataset ha sido trabajado en un '.ipynb' para examinar la relevancia de la existencia de datos nulos en columnas importantes como la referente a la temperatura media, así como para unificar las columnas "Year", "Month" y "Day" en otra columna llamada "Date" y para pasar los nombres de éstas a minúsulas con intención de facilitar el trabajo de los datos. El archivo csv resultado de esta limpieza se encuentra en la carpeta 'output'.

El programa para ser ejecutado en la terminal debe ser "llamado" con "python3 main.py" y recibir alguno de estos cuatro parámetros (argparse):
* '-c': la ciudad de la que quieres obtener la información
* '-s': la fecha por la que quieres empezar a obtener información. En formato mm/dd/yy.
* '-e', la fecha por la que quieres terminar de obtener información.En formato mm/dd/yy.
* '-t', la temperatura (máxima) por la que quieres filtrar la información.

Éste permite obtener un gráfico que muestra la evolución de la temperatura media de la ciudad introducida entre las fechas indicadas, obteniendo la información del dataset importado o de una llamada a la API en función de las fechas señaladas (atendiendo a los límites explicados en párrafos anteriores). En caso de no indicarse ninguna ciudad en concreto, el gráfico se pinta con la temperatura media global.

Las fechas han sido trabajadas en todo momento con el formato 'datetime' para facilitar su uso a lo largo del proyecto.

Por otro lado, ofrece un gráfico con la evolución de las precipitaciones medias en el lugar que se le indique mostrando el cambio de una fecha a otra mediante el diferencial de la cantidad. Y, finalmente, permite filtrar los países a partir de una temperatura máxima indicada, obteniendo, por tanto, un set con los nombres de los países que han igualado y/o superado la misma.

**Por cuestiones de privacidad y seguridad la api-key con la que se ha llevado a cabo el proyecto ha sido retirada del mismo. Para poder ejecutar el programa deberá obtener la suya propia a través del siguiente enlace: [Meteostat api-key](https://auth.meteostat.net)**


© Meteostat 2020 | Legal Disclosure & Privacy| Powered by Meteostat. Raw data provided by NOAA, Deutscher Wetterdienst and others.



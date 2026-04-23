import pandas as pd
from data import url_ps
from data import url_dr


df_feo_ps = pd.read_csv(url_ps)
df_feo_dr = pd.read_csv(url_dr)

#---Limpieza de datos---#

# se eliminan columnas innecesarias y redundantes

def df_ps():
    return (df_feo_ps
    .drop(columns=['time', 'duration']) #elimina columnas
    .loc[lambda df: df['stop']<7] # quita valores mayores a 7
    .groupby(['raceId', 'driverId']) #agrupa conductores y carreras
    .agg(
        stop=('stop', 'max'), #se suman las paradas🥵
        milliseconds=('milliseconds', 'sum') #por cada parada se suman los ms
    )
    .assign(seconds=lambda df:df['milliseconds']/1000) #se transforma en seg
    .drop(columns=['milliseconds']) #Se quita la col de ms
    .reset_index() 
    )

def df_dr():
    return (df_feo_dr
    .drop(columns=['url', 'number', 'code', 'surname']) #elimina columnas
    #viendo valores unicos argentina y argentino se repiten, entonces se reemplazan.
    .assign(nationality=lambda df:df['nationality'].replace('Argentine', 'Argentinian '))
    )

'''
Crear un nuevo dataframe donde el nombre del conductor se identifique en 
con el driverId y se agregue en una nueva columna correspondiente con su
Id de conductor
'''

#---Data wrangling---#


import pandas as pd
from data import url_ps, url_dr, url_stan

import ssl
#Desactivar la verificacion de seguridad SSL
ssl.create_default_https_context = ssl._create_unverified_context

df_feo_ps = pd.read_csv(url_ps)
df_feo_dr = pd.read_csv(url_dr)
df_feo_stan = pd.read_csv(url_stan)

#---Limpieza de datos---#

# se eliminan columnas innecesarias y redundantes

df_ps=(df_feo_ps
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

df_dr=(df_feo_dr
    .drop(columns=['url', 'number', 'code', 'surname', 'dob']) #elimina columnas
    #viendo valores unicos argentina y argentino se repiten, entonces se reemplazan.
    .assign(nationality=lambda df:df['nationality'].replace('Argentine', 'Argentinian '))
    )

df_stan=(df_feo_stan
    .drop(columns=['driverStandingsId', 'positionText', 'points', 'wins']) #Quitar columnas innecesatias
    .loc[lambda df:df['position']<11] #quitar posiciones mayores a 11
    )

'''
Crear un nuevo dataframe donde el nombre del conductor se identifique en 
con el driverId y se agregue en una nueva columna correspondiente con su
Id de conductor
'''

df_ps_dr = df_ps.merge(df_dr, on='driverId', how='left') #Combina Pitstop y Drivers (PsDr)
df_psdrstan = df_ps_dr.merge(df_stan, on=['raceId', 'driverId'], how='left') 
df_psdrstan = df_psdrstan.dropna().reset_index() #Combina PsDr y standings

print(f'---PitStops, Drivers y Standings unidos---\n')
print(f'{df_psdrstan.head()}\n') 

#Aseguramos que no hay ningun valor nulo 
null_counts = df_psdrstan.isnull().sum()
null_percent = (null_counts / len(df_psdrstan)) * 100

missing_data = pd.DataFrame({
    'Valores nulos': null_counts,
    '% del total': null_percent.round(2)
})
print('---Valores nulos---\n')
print(f'{missing_data} \n')

#Se define una funcion para sacar automaticamente la comparacion de las 1ras y ultimas carreras

def compFirstLast(name): #se pide la variable de nombre
    df_name = df_psdrstan[df_psdrstan['driverRef']==name] #busca ddentro de DriverRef el nombre
    df_tail = df_name.tail(10).reset_index() #10 ultimas carreras 
    df_head = df_name.head(10).reset_index() #10 primeras carreras 
    #elimina columnas 
    elim_cols = ['index', 'driverId', 'stop', 'seconds', 'nationality', 'raceId', 'forename']
    df_tail = (df_tail.drop(columns=elim_cols)) 
    df_head = (df_head.drop(columns=elim_cols))
    df_name = pd.concat([df_head, df_tail], axis=1) #Se concatenan
    print(f'---Comparación entre las primeras y ultimas carreras de {name.capitalize()}---\n')
    return df_name


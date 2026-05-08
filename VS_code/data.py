import pandas as pd

import ssl
#Desactivar la verificacion de seguridad SSL
ssl.create_default_https_context = ssl._create_unverified_context

#almacena los datos en la variable df_ps (pit stops)
url_ps = 'https://raw.githubusercontent.com/IvTole/MachineLearning_InferenciaBayesiana_CUGDL/refs/heads/main/data/formula1/pit_stops.csv'

url_dr = 'https://raw.githubusercontent.com/IvTole/MachineLearning_InferenciaBayesiana_CUGDL/refs/heads/main/data/formula1/drivers.csv'

url_stan = 'https://raw.githubusercontent.com/IvTole/MachineLearning_InferenciaBayesiana_CUGDL/refs/heads/main/data/formula1/driver_standings.csv'


#Buscará dentro del df todos los nombres en driverRef que coincidan con hamilton
#df_hamilton = df_psdrstan[df_psdrstan['driverref']=='hamilton']




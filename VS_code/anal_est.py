from data_prep import compFirstLast
import matplotlib.pyplot as plt 

import ssl
#Desactivar la verificacion de seguridad SSL
ssl.create_default_https_context = ssl._create_unverified_context

print(compFirstLast('raikkonen')) #Comparación de las carreras de raikkonen






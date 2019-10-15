#
# Consulta base de dados terremoto 
# em database mongodb.
#

__autor__ = "neviim jads - 2018"
__version__ = "0.0.1"

from pymongo import MongoClient
from hashlib import md5, sha1
from lxml import html
from datetime import datetime
from pytz import timezone
from geopy.geocoders import Nominatim
from pprint import pprint

import requests
import config as cf
import json

# .........


#local = 'Pondaguitan'
#pais  = 'Philippines'
#geolocalizacao = Nominatim(user_agent="terremotos")
#locacao = geolocalizacao.geocode(local, pais)


# conecta ao mongodb, defini collection terremoto
host  = cf.mongodb_host
porta = cf.mongodb_port

client  = MongoClient(host, porta)
db = client.terremotos
collection = db['registros']

# ------------------------
''' Modelo de um registro:

    {'_id': ObjectId('5be0821b57f41c645fc45bdd'),
    'data_bra': '05/11/2018',
    'data_gnt': '05/11/2018',
    'hora_bra': '04:27',
    'hora_gnt': '07:27',
    'intensidade': 'Terremoto Moderado',
    'key': 'f2d23e3a001bf654b6b839330c7be84f86c04840',
    'latitude': '000.000°N',
    'localidade_pais': ['86km SSW of Puerto El Triunfo', ' El Salvador'],
    'longitude': '000.000°W',
    'magnitude': '4.5',
    'profundidade': ['40.43', 'km']
    }
'''

# imprime o primeiro poste registrado.
#pprint(collection.find_one())
#pprint(collection.find_one({"magnitude": "6"}))

# Postagens anteriores a uma determinada data, mas também classificamos os resultados por magnitude:
#d = datetime(2019, 1, 1, 12)
d = "05/11/2018"

for post in collection.find({"data_bra": {"$lt": d}}).sort("magnitude"):
    print()
    pprint(post)


# close.......
client.close()
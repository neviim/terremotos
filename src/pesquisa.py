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
# --------------------------






# close.......
client.close()
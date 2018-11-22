# Carregando a coleção com documentos simples. Criamos um índice em um dos dois atributos:

from pyArango.connection import *
from pyArango.collection import *
 
conn = Connection(username="root", password="root")
        
db = conn["_system"]
 
if not db.hasCollection('test'):
    testCol = db.createCollection('Collection', name='test')
else:
    testCol = db.collections['test']
    testCol.truncate()
 
i = 0
while i < 100000:
    i+=1
    testCol.createDocument({'foo': 'bar', 'count': i, 'counter': i}).save()
 
testCol.ensureHashIndex(['count'], sparse=False)
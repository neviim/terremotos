import sys
import statsd
from pyArango.connection import *
from pyArango.collection import *
 
statsdc = statsd.StatsClient('127.0.0.1', '8125')
conn = Connection(username="root", password="root", statsdClient = statsdc)
db = conn["_system"]
testCol = db.collections['test']
 
transaction = '''
    function(params) {
      var db = require('@arangodb').db;
      var startOne = Date.now();
      var q1 = db._query(`FOR doc IN test FILTER doc.count == @i - 1 RETURN doc`, {i:params.i})
      var startTwo = Date.now()
      var q2 = db._query(`FOR doc IN test FILTER doc.counter == @i - 1 RETURN doc`, {i:params.i})
      var startThree = Date.now()
      var q3 = db._query(`RETURN 1`)
      var end = Date.now();
      return {
        tq1: startTwo - startOne,
        tq2: startThree - startTwo,
        tq3: end - startThree,
        all: end - startOne
      }
    }
'''
 
i = 0
while i < 100000:
    aql = '''
    FOR doc IN test FILTER doc.count == @i - 1 RETURN doc
    '''
    db.AQLQuery(aql, rawResults=True, batchSize=1, count=True, bindVars= {'i' : i})
    times = db.transaction(['test'], transaction, params={'i': i})['result']

    for which in times:
        statsdc.timing(which, times[which])


# For node in nodes
# filter node.name == 104
# return node 

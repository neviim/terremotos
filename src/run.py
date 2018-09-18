# -*- coding: UTF-8 -*-
#
# conda activate py37
# cd c:\Users\jorge.FCN\Documents\GitHub\_python_projetos
# url: http://monitorglobal.com.br/terremotos.html
#
# uso: python run.py
#
# ------------------------------
__autor__ = "neviim jads - 2018"

import alerta_nt7 as tr 

# utilizando class alertaNt7Terremotos estrair dados
url = 'http://monitorglobal.com.br/terremotos.html'
tjson = []

# conecta no site e captura as 200 ultimas ocorrencias
terremotos = tr.AlertaNt7Terremotos(url)
scrap = terremotos.scraping()
listjson = terremotos.cria_json(scrap)

# os insidentes que nao estiver no banco serão gravados.
terremotos.grava_novas_ocorrencias(listjson)

# retorna data e hora local em dois formatos
data1, data2 = terremotos.data_hora()
print(data1, data2)
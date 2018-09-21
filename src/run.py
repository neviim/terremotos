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
at = AlertaNt7Terremotos(url)
ultimos200 = at.get_scraping()
ultimos200_json = at.formato_json(ultimos200)

# os insidentes que nao estiver no banco serão gravados.
#at.grava_novas_ocorrencias(ultimos200_json,'localhost')
at.grava_novas_ocorrencias(ultimos200_json)

# retorna data e hora local em dois formatos
data1, data2 = at.data_hora()
print(data1, data2)
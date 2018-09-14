# -*- coding: UTF-8 -*-
#
# conda activate py37
# cd C:\Users\jorge.FCN\Documents\GitHub\_python_projetos
# url: http://monitorglobal.com.br/terremotos.html
#
''' { 'hora_gmt_utc':  '14/09/2018 08:32', 
      'hora_brasilia': '14/09/2018 05:32', 
      'intensidade': 'Terremoto Leve', 
      'magnitude': '2.9', 
      'profundidade': '9.6 km', 
      'localidade_pais': ['72km SW of Kaktovik', ' Alaska']}

'''
import pandas as pd


path = "../data/terremotos_ultimos10_anos.csv"
df = pd.read_csv(path, skip, thousands=',')

print(df.head(5))
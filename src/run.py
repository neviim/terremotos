# -*- coding: UTF-8 -*-
#
# conda activate py37
# cd C:\Users\jorge.FCN\Documents\GitHub\_python_projetos
#
import pandas as pd


path = "../data/terremotos_ultimos10_anos.csv"
df = pd.read_csv(path, skip, thousands=',')

print(df.head(5))
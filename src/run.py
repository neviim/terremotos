# -*- coding: UTF-8 -*-
#
import pandas as pd


path = "../data/terremotos_ultimos10_anos.csv"
df = pd.read_csv(path, skiprows = 1, thousands=',')

print(df.head(5))
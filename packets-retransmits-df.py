import json
from statsmodels.tsa.stattools import adfuller
import numpy as np

with open('data/packets-retransmits_normalized.json', 'r') as file:
    data = json.load(file)

packets_retransmits_values = np.array([int(entry["val"]) for entry in data])

result = adfuller(packets_retransmits_values)
print('Teste de Estatística ADF: %f' % result[0])
print('p-valor: %f' % result[1])
print('Valores Críticos:')

for key, value in result[4].items():
     print('\t%s: %.3f' % (key, value))
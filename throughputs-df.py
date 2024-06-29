import json
import numpy as np
from statsmodels.tsa.stattools import adfuller

with open('data/throughputs_normalized.json', 'r') as file:
    data = json.load(file)

throughput_values = np.array([int(entry["val"]) for entry in data])

result = adfuller(throughput_values)
print('Teste de Estatística ADF (Throughput): %f' % result[0])
print('p-valor: %f' % result[1])
print('Valores Críticos:')

for key, value in result[4].items():
     print('\t%s: %.3f' % (key, value))
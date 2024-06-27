import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

with open('data/packets-retransmits.json', 'r') as file:
    data = json.load(file)

# Extract timestamps and values
timestamps = []
values = []

for item in data:
    timestamps.append(datetime.fromtimestamp(item["ts"]))
    values.append(item["val"])

plt.switch_backend('TkAgg')
plt.figure(figsize=(15, 5))
plt.plot(timestamps, values, linestyle='-')

date_format = mdates.DateFormatter("%d/%m/%Y")
plt.gca().xaxis.set_major_formatter(date_format)

# Plot the data
plt.xlabel("Dia do Ano", fontsize=16)
plt.ylabel("Quantidade de Retransmissões", fontsize=16)
plt.title("Retransmissões (RNP SP para RNP RS)", fontsize=18)
plt.legend()
plt.grid(True)
plt.show()
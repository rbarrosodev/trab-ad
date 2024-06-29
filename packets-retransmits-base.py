import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

with open('data/packets-retransmits.json', 'r') as file:
    data = json.load(file)

timestamps = [datetime.fromtimestamp(item["ts"]) for item in data]
values = [item["val"] for item in data]

plt.switch_backend('TkAgg')
plt.figure(figsize=(15, 5))
plt.plot(timestamps, values, linestyle='-')

date_format = mdates.DateFormatter("%d/%m/%Y")
plt.gca().xaxis.set_major_formatter(date_format)

# Plot the data
plt.xlabel("Dia do Ano", fontsize=16)
plt.ylabel("Retransmissões", fontsize=16)
plt.title("Retransmissões (POP SP para POP RS)", fontsize=18)
plt.legend()
plt.grid(True)
plt.show()
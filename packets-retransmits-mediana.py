import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


def remove_outliers(packet_reetransmits, m=2.):
    values = [int(entry["val"]) for entry in packet_reetransmits]

    value_array = np.array(values)
    d = np.abs(value_array - np.median(value_array))
    mdev = np.median(d)
    s = d / (mdev if mdev else 1.)

    result_data = []
    for i, value in enumerate(s < m):
        if value:
            result_data.append(packet_reetransmits[i])

    return result_data


with open('data/packets-retransmits.json', 'r') as file:
    packet_retransmits_data = json.load(file)

normalized_data = remove_outliers(packet_retransmits_data)
normalized_data_bkp = [{"ts": entry["ts"], "val": entry["val"]} for entry in normalized_data]

for data in normalized_data:
    data["ts"] = datetime.fromtimestamp(data["ts"])

timestamps = [data["ts"] for data in normalized_data]
values = [data["val"] for data in normalized_data]

plt.figure(figsize=(15, 5))
plt.plot(timestamps, values)

date_format = mdates.DateFormatter("%d/%m/%Y")
plt.gca().xaxis.set_major_formatter(date_format)

plt.grid(True)
plt.ylim(0, 600)
plt.xlabel("Dia do Ano", fontsize=16, labelpad=10)
plt.ylabel("Retransmissões", fontsize=16)
plt.title("Retransmissões (Normalizadas por Mediana) [POP SP para POP RS]", fontsize=18)

# Show the plot
plt.show()

json_object = json.dumps(normalized_data_bkp, indent=4)
with open("data/packets-retransmits_normalized.json", "w") as outfile:
    outfile.write(json_object)
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import json


def remove_outliers(throughputs, m=2.):
    values = [int(entry["val"]) for entry in throughputs]

    value_array = np.array(values)
    d = np.abs(value_array - np.median(value_array))
    mdev = np.median(d)
    s = d / (mdev if mdev else 1.)

    result_data = []
    for i, value in enumerate(s < m):
        if value:
            result_data.append(throughputs[i])

    return result_data


with open('data/throughputs.json', 'r') as file:
    throughputs_data = json.load(file)

normalized_throughputs = remove_outliers(throughputs_data)
normalized_throughputs_bkp = [{"ts": entry["ts"], "val": entry["val"]} for entry in normalized_throughputs]

for data in normalized_throughputs:
    data["ts"] = datetime.fromtimestamp(data["ts"])

timestamps = [data["ts"] for data in normalized_throughputs]
values = [data["val"] / 1000000000 for data in normalized_throughputs]

plt.figure(figsize=(15, 5))
plt.plot(timestamps, values)

date_format = mdates.DateFormatter("%d/%m/%Y")
plt.gca().xaxis.set_major_formatter(date_format)

plt.grid(True)
plt.ylim(0, 5)
plt.xlabel("Dia do Ano", fontsize=16, labelpad=10)
plt.ylabel("Gbits/s", fontsize=16)
plt.title("Taxa de Transferência (Normalizada por Mediana) [POP SP para POP RS]", fontsize=18)

# Show the plot
plt.show()

json_object = json.dumps(normalized_throughputs_bkp, indent=4)
with open("data/throughputs_normalized.json", "w") as outfile:
    outfile.write(json_object)
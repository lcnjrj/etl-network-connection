import pandas as pd
from datetime import datetime

records = []

with open("network_logs.txt") as f:
    for line in f:
        if "state change" in line and "device (" in line:
            parts = line.split()

            # data/hora (jan 08 03:39:24)
            try:
                date_str = f"{parts[0].title()} {parts[1]} {parts[2]}"
                dt = datetime.strptime(date_str, "%b %d %H:%M:%S")
                dt = dt.replace(year=datetime.now().year)
            except:
                continue

            # interface
            iface = line.split("device (")[1].split(")")[0]

            # estado
            state = line.split("->")[-1].split("(")[0].strip()

            # tipo de conexão
            if iface.startswith("wl"):
                conn_type = "Wi-Fi"
            elif iface.startswith("en"):
                conn_type = "Cabeada"
            else:
                continue  # ignora lo, macs, etc

            records.append({
                "datetime": dt,
                "iface": iface,
                "connection_type": conn_type,
                "state": state
            })

df = pd.DataFrame(records).sort_values("datetime")

df["duration_minutes"] = (
    df["datetime"].diff().dt.total_seconds() / 60
).round(2)

df.to_csv("network_report.csv", index=False)

print("Registros gerados:", len(df))

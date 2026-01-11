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

dt = datetime.strptime(
    f"{parts[0].title()} {parts[1]} {datetime.now().year} {parts[2]}",
    "%b %d %Y %H:%M:%S"
)
df["duration_minutes"] = None

last_activated = None

for i, row in df.iterrows():
    if row["state"] == "activated":
        last_activated = row["datetime"]
    elif row["state"] in ("disconnected", "unavailable") and last_activated:
        df.at[i, "duration_minutes"] = round(
            (row["datetime"] - last_activated).total_seconds() / 60, 2
        )
        last_activated = None


print("Registros gerados:", len(df))

import pandas as pd
from datetime import datetime

records = []

with open("network_logs.txt") as f:
    for line in f:
        if "state change" in line and "device (" in line:
            parts = line.split()

            # data/hora com ano explícito (corrige warning)
            try:
                date_str = f"{parts[0].title()} {parts[1]} {datetime.now().year} {parts[2]}"
                dt = datetime.strptime(date_str, "%b %d %Y %H:%M:%S")
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
                continue  # ignora lo, MAC puro, etc

            records.append({
                "datetime": dt,
                "iface": iface,
                "connection_type": conn_type,
                "state": state
            })

# === TRANSFORM ===
df = pd.DataFrame(records).sort_values("datetime")

df["duration_minutes"] = None

last_activated = {}

for idx, row in df.iterrows():
    iface = row["iface"]

    if row["state"] == "activated":
        last_activated[iface] = row["datetime"]

    elif row["state"] in ("disconnected", "unavailable") and iface in last_activated:
        df.at[idx, "duration_minutes"] = round(
            (row["datetime"] - last_activated[iface]).total_seconds() / 60, 2
        )
        del last_activated[iface]

# === LOAD ===
df.to_csv("network_report.csv", index=False)

print("Registros gerados:", len(df))

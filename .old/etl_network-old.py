import re
import pandas as pd
from datetime import datetime

log_file = "network_logs.txt"

pattern = re.compile(
    r'(?P<date>\w{3} \d{2} \d{2}:\d{2}:\d{2}).*device \((?P<iface>.*?)\): state change: .* -> (?P<state>\w+)'
)

records = []

with open(log_file) as f:
    for line in f:
        match = pattern.search(line)
        if match:
            data = match.groupdict()
            data["datetime"] = datetime.strptime(
                data["date"], "%b %d %H:%M:%S"
            ).replace(year=datetime.now().year)

            # tipo de conexão
            if data["iface"].startswith("wl"):
                data["connection_type"] = "Wi-Fi"
            elif data["iface"].startswith("en"):
                data["connection_type"] = "Cabeada"
            else:
                data["connection_type"] = "Outro"

            records.append(data)

print(f"Registros extraídos: {len(records)}")
df = pd.DataFrame(records)
df = df.sort_values("datetime")

# Calcular duração
df["prev_time"] = df["datetime"].shift(1)
df["duration_minutes"] = (
    (df["datetime"] - df["prev_time"]).dt.total_seconds() / 60
).round(2)

# Manter apenas eventos relevantes
df_final = df[["datetime", "iface", "connection_type", "state", "duration_minutes"]]

df_final.to_csv("network_report.csv", index=False)

print(df_final.head())

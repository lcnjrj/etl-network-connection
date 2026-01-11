import pandas as pd

df = pd.read_csv("network_report.csv")

print(
    df.groupby("connection_type")["duration_minutes"].sum()
)

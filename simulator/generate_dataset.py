import pandas as pd
from sensors import MachineSimulator

N = 20000

machine = MachineSimulator("M1", fault_prob=0.005)
rows = [machine.read() for _ in range(N)]

df = pd.DataFrame(rows)
df["timestamp"] = pd.date_range("2026-01-01", periods=N, freq="s")

df.to_csv("data/dataset.csv", index=False)

print(df.head())
print("\nTotal :", len(df))
print("Répartition normal / panne :")
print(df["fault"].value_counts())
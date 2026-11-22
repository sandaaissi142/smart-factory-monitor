import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("data/dataset.csv", parse_dates=["timestamp"])

# On affiche les 4000 premières secondes pour que ce soit lisible
d = df.iloc[:4000]
sensors = ["temperature", "vibration", "current", "pressure"]
units = {"temperature": "°C", "vibration": "mm/s", "current": "A", "pressure": "bar"}

fig = make_subplots(
    rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.05,
    subplot_titles=[f"{s.capitalize()} ({units[s]})" for s in sensors],
)

for i, s in enumerate(sensors, start=1):
    normal = d[d["fault"] == 0]
    panne = d[d["fault"] == 1]
    fig.add_trace(
        go.Scattergl(x=normal["timestamp"], y=normal[s], mode="markers",
                     marker=dict(size=3, color="#2563eb"), name="Normal",
                     showlegend=(i == 1)),
        row=i, col=1,
    )
    fig.add_trace(
        go.Scattergl(x=panne["timestamp"], y=panne[s], mode="markers",
                     marker=dict(size=4, color="#dc2626"), name="Panne",
                     showlegend=(i == 1)),
        row=i, col=1,
    )

fig.update_layout(
    title="Smart Factory Monitor : données capteurs simulées (normal vs panne)",
    height=900, width=1300, template="plotly_white",
    legend=dict(orientation="h", y=1.06),
)

fig.write_html("data/dataset_plot.html")
fig.show()
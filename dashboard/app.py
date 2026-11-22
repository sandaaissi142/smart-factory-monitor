import json
import threading
import time
from collections import deque

import joblib
import paho.mqtt.client as mqtt
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

FEATURES = ["temperature", "vibration", "current", "pressure"]
UNITS = {"temperature": "°C", "vibration": "mm/s", "current": "A", "pressure": "bar"}
BROKER = "localhost"
TOPIC = "factory/M1/sensors"

st.set_page_config(page_title="Smart Factory Monitor", layout="wide")


@st.cache_resource
def load_model():
    return joblib.load("model/model.joblib")


@st.cache_resource
def start_subscriber():
    buffer = deque(maxlen=300)
    lock = threading.Lock()

    def on_message(client, userdata, msg):
        with lock:
            buffer.append(json.loads(msg.payload))

    def on_connect(client, userdata, flags, reason_code, properties):
        client.subscribe(TOPIC)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, 1883)
    client.loop_start()
    return buffer, lock


model = load_model()
buffer, lock = start_subscriber()

st.title("🏭 Smart Factory Monitor")
st.caption("Maintenance prédictive IoT · capteurs simulés → MQTT → Isolation Forest")

with lock:
    data = list(buffer)

if len(data) < 10:
    st.info("En attente des données... lance le publisher.")
    time.sleep(1)
    st.rerun()

df = pd.DataFrame(data)
df["anomaly"] = model.predict(df[FEATURES]) == -1

last = df.iloc[-1]
prev = df.iloc[-2]
recent_anomalies = int(df.tail(10)["anomaly"].sum())
alert = recent_anomalies >= 5

if alert:
    st.error(f"🚨 ALERTE : comportement anormal détecté ({recent_anomalies}/10 dernières mesures)")
else:
    st.success("✅ Machine M1 : fonctionnement normal")

cols = st.columns(5)
for col, s in zip(cols[:4], FEATURES):
    col.metric(f"{s.capitalize()} ({UNITS[s]})", f"{last[s]:.2f}", f"{last[s] - prev[s]:+.2f}")
cols[4].metric("Anomalies (300 dernières mesures)", int(df["anomaly"].sum()))

fig = make_subplots(
    rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.06,
    subplot_titles=[f"{s.capitalize()} ({UNITS[s]})" for s in FEATURES],
)
x = list(range(len(df)))
for i, s in enumerate(FEATURES, start=1):
    fig.add_trace(
        go.Scatter(x=x, y=df[s], mode="lines", line=dict(color="#2563eb", width=1.5),
                   name=s, showlegend=False),
        row=i, col=1,
    )
    an = df[df["anomaly"]]
    fig.add_trace(
        go.Scatter(x=an.index, y=an[s], mode="markers",
                   marker=dict(color="#dc2626", size=7), name="Anomalie",
                   showlegend=(i == 1)),
        row=i, col=1,
    )
fig.update_layout(height=750, template="plotly_white", margin=dict(t=40, b=10),
                  legend=dict(orientation="h", y=1.05))

st.plotly_chart(fig, width="stretch")

time.sleep(1)
st.rerun()
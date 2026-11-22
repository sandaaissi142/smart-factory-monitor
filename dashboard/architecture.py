import webbrowser
from pathlib import Path

HTML = """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<style>
  body { background:#e5e7eb; font-family: 'Segoe UI', Arial, sans-serif; margin:0; padding:30px; }
  .card { width:1000px; margin:auto; background:#fff; border-radius:16px; padding:40px 48px; box-shadow:0 4px 20px rgba(0,0,0,.08); }
  .tag { color:#2563eb; font-size:13px; font-weight:700; letter-spacing:1.5px; }
  h1 { font-size:42px; margin:8px 0 6px; color:#0f172a; }
  h1 span { color:#2563eb; }
  .sub { color:#64748b; font-size:17px; margin-bottom:34px; }
  .flow { display:flex; align-items:stretch; gap:10px; }
  .box { flex:1; border:2px solid #dbeafe; background:#f8fbff; border-radius:12px; padding:18px 14px; text-align:center; }
  .box b { display:block; font-size:17px; color:#0f172a; margin-bottom:6px; }
  .box small { color:#64748b; font-size:13px; line-height:1.4; }
  .box.ai { border-color:#2563eb; background:#eff6ff; }
  .box.alert { border-color:#fecaca; background:#fef2f2; }
  .arrow { align-self:center; font-size:26px; color:#2563eb; }
  .stats { display:flex; gap:14px; margin-top:34px; }
  .stat { flex:1; border:1px solid #e2e8f0; border-radius:12px; padding:16px; text-align:center; }
  .stat .n { font-size:34px; font-weight:800; color:#2563eb; }
  .stat .l { font-size:13px; color:#64748b; margin-top:2px; }
  .foot { margin-top:30px; display:flex; justify-content:space-between; font-size:14px; color:#475569; border-top:1px solid #e2e8f0; padding-top:16px; }
</style></head><body>
<div class="card">
  <div class="tag">MAINTENANCE PRÉDICTIVE · ARCHITECTURE</div>
  <h1>De la donnée capteur à l'<span>alerte</span> avec l'IA</h1>
  <div class="sub">Pipeline IoT complet, 100 % simulé sur PC</div>

  <div class="flow">
    <div class="box"><b>🌡️ Capteurs</b><small>Température<br>Vibration<br>Courant · Pression<br>(simulés en Python)</small></div>
    <div class="arrow">→</div>
    <div class="box"><b>📡 MQTT</b><small>Broker Mosquitto<br>Topic<br>factory/M1/sensors</small></div>
    <div class="arrow">→</div>
    <div class="box ai"><b>🤖 Isolation Forest</b><small>Détection d'anomalies<br>scikit-learn<br>en temps réel</small></div>
    <div class="arrow">→</div>
    <div class="box"><b>📊 Dashboard</b><small>Streamlit + Plotly<br>Courbes live<br>Indicateurs</small></div>
    <div class="arrow">→</div>
    <div class="box alert"><b>🚨 Alerte</b><small>Déclenchée si ≥ 5<br>anomalies sur<br>10 mesures</small></div>
  </div>

  <div class="stats">
    <div class="stat"><div class="n">4</div><div class="l">capteurs simulés</div></div>
    <div class="stat"><div class="n">93 %</div><div class="l">accuracy</div></div>
    <div class="stat"><div class="n">66 %</div><div class="l">rappel sur les pannes</div></div>
    <div class="n">20 000</div><div class="l">mesures générées</div>
  </div>

  <div class="foot">
    <div><b>Stack</b> · Python · MQTT · Mosquitto · Scikit-learn · Streamlit · Plotly</div>
    <div>Sinda Aissi</div>
  </div>
</div>
</body></html>"""

path = Path("data/architecture.html").resolve()
path.write_text(HTML, encoding="utf-8")
webbrowser.open(path.as_uri())
print("Créé :", path)
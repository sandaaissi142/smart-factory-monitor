import joblib
import pandas as pd
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score

FEATURES = ["temperature", "vibration", "current", "pressure"]

df = pd.read_csv("data/dataset.csv")
split = int(len(df) * 0.7)
test = df.iloc[split:]

model = joblib.load("model/model.joblib")
y_true = test["fault"]
y_pred = (model.predict(test[FEATURES]) == -1).astype(int)

cm = confusion_matrix(y_true, y_pred)
acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred)
rec = recall_score(y_true, y_pred)

labels = ["Normal", "Panne"]
fig = go.Figure(go.Heatmap(
    z=cm, x=[f"Prédit : {l}" for l in labels], y=[f"Réel : {l}" for l in labels],
    text=cm, texttemplate="%{text}", textfont=dict(size=34),
    colorscale="Blues", showscale=False,
))
fig.update_yaxes(autorange="reversed")
fig.update_layout(
    title=(f"Isolation Forest : matrice de confusion<br>"
           f"<sup>Accuracy {acc:.0%} · Précision pannes {prec:.0%} · "
           f"Rappel pannes {rec:.0%}</sup>"),
    width=800, height=650, template="plotly_white",
)

fig.write_html("data/confusion_matrix.html")
fig.show()
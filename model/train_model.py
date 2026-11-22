import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["temperature", "vibration", "current", "pressure"]

df = pd.read_csv("data/dataset.csv")

# Découpage chronologique : 70 % entraînement, 30 % test
split = int(len(df) * 0.7)
train = df.iloc[:split]
test = df.iloc[split:]

# Entraînement sur le fonctionnement normal uniquement
X_train = train[train["fault"] == 0][FEATURES]

model = make_pipeline(
    StandardScaler(),
    IsolationForest(n_estimators=200, contamination=0.03, random_state=42),
)
model.fit(X_train)

# Test : -1 = anomalie détectée, converti en 1
y_true = test["fault"]
y_pred = (model.predict(test[FEATURES]) == -1).astype(int)

print("Matrice de confusion (lignes = réel, colonnes = prédit) :")
print(confusion_matrix(y_true, y_pred))
print()
print(classification_report(y_true, y_pred, target_names=["Normal", "Panne"]))

joblib.dump(model, "model/model.joblib")
print("Modèle sauvegardé : model/model.joblib")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import joblib, json

# 1. Load data
with open("data/intents.json") as f:
    intents = json.load(f)

X, y = [], []
for intent, examples in intents.items():
    X += examples
    y += [intent] * len(examples)

# 2–3. Build & train
pipeline = make_pipeline(
    TfidfVectorizer(),
    LogisticRegression(max_iter=1000)
)
pipeline.fit(X, y)

# 4. Persist
joblib.dump(pipeline, "models/intent_pipeline.joblib")
print("Intent model trained and saved to models/intent_pipeline.joblib")
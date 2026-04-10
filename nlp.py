import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

find_samples = ["where is my wallet", "find my keys"] * 50
update_samples = ["i kept my wallet on table", "keys are in kitchen"] * 50

X = find_samples + update_samples
y = ["FIND"] * len(find_samples) + ["UPDATE"] * len(update_samples)

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vec, y)

def detect_intent(text):
    return model.predict(vectorizer.transform([text]))[0]

def extract_item(text):
    match = re.search(r"my (\w+)", text.lower())
    return match.group(1) if match else None

def extract_location(text):
    match = re.search(r"(on|in|at|near) ([a-zA-Z ]+)", text.lower())
    return match.group(2) if match else None
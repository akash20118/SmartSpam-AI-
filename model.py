import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("spam.csv")

# Features and Labels
X = data["message"]
y = data["label"]

# Convert text into numbers
vectorizer = TfidfVectorizer()

X_vector = vectorizer.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X_vector,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = MultinomialNB()

model.fit(X_train, y_train)

# Calculate Accuracy
y_pred = model.predict(X_test)

accuracy = round(
    accuracy_score(y_test, y_pred) * 100,
    2
)

print("Model Accuracy:", accuracy, "%")


def predict_message(message):

    vector = vectorizer.transform([message])

    result = model.predict(vector)[0]

    probability = model.predict_proba(vector)

    confidence = round(
        max(probability[0]) * 100,
        2
    )

    text = message.lower()

    # Category Detection
    if any(word in text for word in [
        "win",
        "prize",
        "lottery",
        "reward"
    ]):
        category = "Lottery Scam"

    elif any(word in text for word in [
        "bank",
        "account",
        "verify",
        "password"
    ]):
        category = "Phishing Attack"

    elif any(word in text for word in [
        "job",
        "salary",
        "interview"
    ]):
        category = "Job Scam"

    elif any(word in text for word in [
        "offer",
        "discount",
        "sale"
    ]):
        category = "Advertisement"

    else:
        category = "General Spam"

    # Risk Level
    if confidence >= 80:
        risk = "HIGH"

    elif confidence >= 50:
        risk = "MEDIUM"

    else:
        risk = "LOW"

    # Reasons
    reasons = []

    keywords = [
        "win",
        "prize",
        "click",
        "offer",
        "free",
        "bank",
        "password",
        "verify",
        "reward",
        "money"
    ]

    for word in keywords:

        if word in text:

            reasons.append(
                f"Contains keyword: {word}"
            )

    if len(reasons) == 0:

        reasons.append(
            "No suspicious keywords detected"
        )

    # URL Detection
    urls = []

    words = message.split()

    for word in words:

        if (
            word.startswith("http://")
            or
            word.startswith("https://")
        ):

            urls.append(word)

    return (
        result,
        confidence,
        category,
        reasons,
        risk,
        urls
    )
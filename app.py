from flask import Flask, request, render_template, jsonify
import joblib
import re
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from db import get_connection
import os

# Configure NLTK data path BEFORE any NLTK operations
nltk.data.path.append('/opt/render/nltk_data')

print("Loading ML model...")

DISORDER_INFO = {
    "adhd": {
        "symptoms": [
            "Difficulty focusing",
            "Impulsivity",
            "Restlessness",
            "Poor time management"
        ],
        "resources": [
            "Structured daily routines",
            "Behavioral therapy",
            "Professional evaluation"
        ]
    },
    "depression": {
        "symptoms": [
            "Persistent sadness",
            "Low energy",
            "Loss of interest",
            "Sleep problems"
        ],
        "resources": [
            "Counseling or therapy",
            "Physical activity",
            "Social support"
        ]
    },
    "ocd": {
        "symptoms": [
            "Intrusive thoughts",
            "Compulsive behaviors",
            "Anxiety if rituals are avoided"
        ],
        "resources": [
            "CBT with exposure therapy",
            "Mindfulness techniques"
        ]
    },
    "ptsd": {
        "symptoms": [
            "Flashbacks",
            "Nightmares",
            "Hypervigilance"
        ],
        "resources": [
            "Trauma-focused therapy",
            "Grounding techniques"
        ]
    },
    "aspergers": {
        "symptoms": [
            "Difficulty with social interaction",
            "Repetitive behaviors",
            "Strong focus on specific interests"
        ],
        "resources": [
            "Social skills training",
            "Professional guidance"
        ]
    },
    "healthy": {
        "symptoms": [],
        "resources": [
            "Maintain healthy habits",
            "Continue self-care"
        ]
    }
}

# ------------------ Flask ------------------
app = Flask(__name__)

# ------------------ Load model ------------------
clf = None
vectorizer = None
lemmatizer = None

def load_models():
    """Load ML models and NLTK resources on startup"""
    global clf, vectorizer, lemmatizer
    if clf is None:
        print("Preloading ML model...")
        clf = joblib.load("model/logreg_model.pkl")
        vectorizer = joblib.load("model/tfidf_vectorizer.pkl")
        print("Model loaded successfully!")
    
    if lemmatizer is None:
        print("Initializing NLTK lemmatizer...")
        # Download NLTK data if not available
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            print("Downloading wordnet...")
            try:
                nltk.download('wordnet', download_dir='/opt/render/nltk_data')
            except Exception:
                nltk.download('wordnet')
        
        try:
            nltk.data.find('corpora/omw-1.4')
        except LookupError:
            print("Downloading omw-1.4...")
            try:
                nltk.download('omw-1.4', download_dir='/opt/render/nltk_data')
            except Exception:
                nltk.download('omw-1.4')
        
        lemmatizer = WordNetLemmatizer()
        print("Lemmatizer initialized successfully!")

# Load models immediately when module is imported
load_models()

# ------------------ Clean text ------------------
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return " ".join(lemmatizer.lemmatize(w) for w in text.split())

# ------------------ Predict ------------------
def predict_disorder(text):
    cleaned = clean_text(text)
    vec = vectorizer.transform([cleaned])
    probs = clf.predict_proba(vec)[0]
    # top 2 classes
    top2 = probs.argsort()[-2:][::-1]
    best = probs[top2[0]]
    second = probs[top2[1]]
    pred_class = clf.classes_[top2[0]]
    # decision rule
    if best < 0.5 or (best - second) < 0.1:
        return "healthy", best, probs
    return pred_class, best, probs

# ------------------ Database ------------------
def save_prediction(text, label, confidence):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Detect DB type
        if conn.__class__.__module__ == "sqlite3":
            query = """
            INSERT INTO predictions (user_text, predicted_label, confidence)
            VALUES (?, ?, ?)
            """
            cursor.execute(query, (text, label, float(confidence)))
        else:
            query = """
            INSERT INTO predictions (user_text, predicted_label, confidence)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (text, label, float(confidence)))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("DB Error:", e)

# ------------------ Routes ------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400
    
    label, conf, probs = predict_disorder(data["text"])
    save_prediction(data["text"], label, conf)
    
    info = DISORDER_INFO.get(label, {"symptoms": [], "resources": []})
    
    return jsonify({
        "primary_prediction": {
            "disorder": label,
            "confidence": conf,
            "symptoms": info["symptoms"],
            "resources": info["resources"]
        },
        "all_predictions": [
            {
                "disorder": cls,
                "percentage": f"{p*100:.2f}%"
            }
            for cls, p in zip(clf.classes_, probs)
        ]
    })

@app.route("/health")
def health():
    return "ok", 200

@app.route("/debug/db")
def debug_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, predicted_label, confidence, created_at FROM predictions ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"rows": rows}
    except Exception as e:
        return {"error": str(e)}

application = app

if __name__ == "__main__":
    app.run(debug=True)

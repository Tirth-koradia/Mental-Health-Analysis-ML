# 🧠 Mental Health Analysis System (NLP + ML + Flask + MySQL)

A web-based machine learning application that analyzes user text and predicts potential mental health conditions using Natural Language Processing.

---

## 🚀 Features
- Multi-class mental health classification (ADHD, Depression, OCD, PTSD, Aspergers, Healthy)
- TF-IDF text vectorization
- Logistic Regression probabilistic prediction
- Confidence score output
- REST API endpoint
- MySQL database storage of predictions
- Interactive web interface

---

## 📊 Model Performance
| Metric | Value |
|------|------|
| Accuracy | ~82% |
| Macro F1 Score | ~0.84 |
| Test Samples | 17,000+ |

---

## 🛠 Tech Stack
- Python
- Flask
- Scikit-learn
- NLP (TF-IDF + Lemmatization)
- MySQL

---

## 📁 Project Structure
```
app.py              # Flask backend + API
model/              # Trained ML model files
templates/          # Frontend UI (HTML)
db/schema.sql       # Database schema
```

---

## ▶️ Run Locally

### Install dependencies
```bash
pip install -r requirements.txt
```

### Start server
```bash
python app.py
```

Open in browser:
```
http://127.0.0.1:5000
```

---

## 🔌 API Endpoint

**POST** `/api/predict`

```json
{
  "text": "I feel anxious and can't focus"
}
```

---

## ⚠️ Disclaimer
This project is for educational purposes only and is **not a medical diagnosis tool**.
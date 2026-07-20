# 🩺 Diabetes Risk Prediction API

A production-ready **FastAPI** application for diabetes risk prediction using machine learning models. The project provides a RESTful API, automatic request validation, interactive API documentation, and a lightweight web interface for real-time inference.

---

## Features

- FastAPI REST API
- Machine Learning–based diabetes prediction
- Two prediction models (Production & Pipeline)
- Automatic request validation with Pydantic
- Interactive Swagger & ReDoc documentation
- HTML/CSS/JavaScript frontend
- Health and model status endpoints
- Modular backend architecture
- Ready for cloud deployment

---

## Tech Stack

### Backend
- FastAPI
- Uvicorn
- Pydantic
- Scikit-learn
- XGBoost
- NumPy
- Pandas

### Frontend
- HTML5
- CSS3
- JavaScript

### Machine Learning
- XGBoost
- Pickle (.pkl)

---

## Project Structure

```text
diabetes-fastapi/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── routers/
│   ├── services/
│   ├── models/
│   ├── templates/
│   └── static/
│
├── ml_models/
├── requirements.txt
├── run.py
└── README.md
```

---

## Machine Learning Models

### Model V1 (Production)

**File**

```
xgb_diabetes_model6.pkl
```

**Features**

- Age
- BMI
- Gender
- Hypertension
- Heart Disease
- Smoking History
- HbA1c Level
- Blood Glucose Level

---

### Model V2 (Pipeline)

**File**

```
diabetes_pipeline(1).pkl
```

Uses the complete feature pipeline from the original training dataset to maintain prediction compatibility.

---

## Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/diabetes-fastapi.git
cd diabetes-fastapi
```

### Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Add model files

Place the trained `.pkl` files inside:

```text
ml_models/
```

---

## Running the Application

```bash
python run.py
```

or

```bash
uvicorn app.main:app --reload
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Web Interface |
| GET | `/docs` | Swagger UI |
| GET | `/redoc` | ReDoc Documentation |
| GET | `/health` | Health Check |
| GET | `/api/predict/status` | Model Status |
| POST | `/api/predict/v1` | Production Model |
| POST | `/api/predict/v2` | Pipeline Model |





## License

This project is licensed under the MIT License.

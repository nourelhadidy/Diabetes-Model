# 🩺 Diabetes Risk Prediction API

> A production-ready machine learning web application for diabetes risk prediction built with **FastAPI**, **XGBoost**, and a modern HTML/CSS/JavaScript frontend.

The project transforms an original Streamlit prototype into a scalable REST API by separating machine learning inference from the presentation layer. It provides interactive API documentation, automatic request validation, health monitoring, and a lightweight web interface for real-time predictions.

---

## 📖 Overview

This application predicts a patient's risk of diabetes using trained machine learning models.

Key improvements over the original Streamlit implementation include:

- RESTful API using FastAPI
- Modular backend architecture
- Automatic request validation with Pydantic
- Interactive Swagger and ReDoc documentation
- Models loaded once at startup for improved performance
- Separation of business logic from HTTP endpoints
- Responsive web interface
- Easily deployable to cloud platforms

---

## ✨ Features

- 🧠 Machine Learning diabetes prediction
- ⚡ High-performance FastAPI backend
- 📄 Automatic Swagger & ReDoc API documentation
- ✅ Input validation using Pydantic
- 🌐 Responsive HTML/CSS/JavaScript frontend
- 📊 Prediction probability and risk classification
- ❤️ Health check endpoint
- 📦 Modular, production-ready architecture
- 🚀 Ready for cloud deployment

---

## 🏗️ System Architecture

```
                    User
                     │
                     ▼
        HTML / CSS / JavaScript Frontend
                     │
             HTTP Requests (JSON)
                     │
                     ▼
              FastAPI Application
                     │
      ┌──────────────┴──────────────┐
      │                             │
      ▼                             ▼
 Prediction Router             Static Pages
      │
      ▼
 Prediction Service
      │
      ▼
 Machine Learning Models (.pkl)
      │
      ▼
 Prediction Response
```

---

# 📁 Project Structure

```
diabetes-fastapi/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── routers/
│   │   ├── predict.py
│   │   └── pages.py
│   │
│   ├── services/
│   │   └── prediction.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── style.css
│       └── app.js
│
├── ml_models/
│   ├── xgb_diabetes_model6.pkl
│   ├── diabetes_pipeline(1).pkl
│   └── README.md
│
├── requirements.txt
├── run.py
└── README.md
```

---

# 🏛️ Backend Architecture

### `services/`

Contains all machine learning inference logic.

Responsibilities:

- Load trained models
- Feature engineering
- Data preprocessing
- Prediction
- Probability estimation

No HTTP-related code exists here, making it reusable and testable.

---

### `routers/`

Defines API endpoints.

Responsibilities:

- Receive requests
- Validate inputs
- Call prediction services
- Return JSON responses
- Handle HTTP errors

Business logic is intentionally excluded.

---

### `schemas.py`

Uses **Pydantic** models to validate incoming requests.

Benefits include:

- Automatic type checking
- Required field validation
- Value constraints
- Auto-generated API documentation
- Prevents invalid data from reaching the model

---

### Model Loading

Unlike Streamlit, models are loaded **once during application startup**, eliminating repeated disk reads and significantly reducing prediction latency.

---

# 🧠 Machine Learning Models

## Version 1

Production XGBoost model

```
xgb_diabetes_model6.pkl
```

Uses a clean feature set:

- Age
- BMI
- Hypertension
- Heart Disease
- Smoking History
- HbA1c Level
- Blood Glucose Level
- Gender

---

## Version 2

Pipeline model preserving the original training workflow.

```
diabetes_pipeline(1).pkl
```

Maintains duplicated columns from the training dataset to ensure identical predictions.

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/USERNAME/diabetes-fastapi.git

cd diabetes-fastapi
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Add Machine Learning Models

Copy all required `.pkl` files into

```
ml_models/
```

---

# ▶️ Running the Application

```bash
python run.py
```

or

```bash
uvicorn app.main:app --reload
```

---

# 🌐 Available Endpoints

| Endpoint | Description |
|-----------|-------------|
| `/` | Web Interface |
| `/docs` | Swagger UI |
| `/redoc` | ReDoc Documentation |
| `/health` | Health Check |
| `/api/predict/status` | Model Status |
| `/api/predict/v1` | Prediction API (Model V1) |
| `/api/predict/v2` | Prediction API (Model V2) |

---

# 📡 API Usage

## POST `/api/predict/v1`

### Request

```json
{
  "age": 45,
  "bmi": 27.5,
  "hypertension": 0,
  "heart_disease": 0,
  "smoking_history": 0,
  "hba1c_level": 5.6,
  "blood_glucose_level": 110,
  "gender": 0
}
```

---

## Response

```json
{
  "probability": 0.1234,
  "prediction": 0,
  "risk_label": "Low Risk of Diabetes",
  "threshold_used": 0.5,
  "model_version": "v1-xgb-model6"
}
```

---

## POST `/api/predict/v2`

Supports the original training pipeline using the complete feature set.

---

# 📊 Prediction Output

Every prediction returns:

- Prediction
- Probability
- Risk Label
- Threshold
- Model Version

---

# 🔍 Why FastAPI?

Compared to the original Streamlit implementation, FastAPI provides:

| Streamlit | FastAPI |
|------------|----------|
| UI and logic tightly coupled | Fully separated architecture |
| Script reruns every interaction | Models loaded once |
| Difficult to integrate | REST API |
| Limited validation | Pydantic validation |
| UI-focused | Production backend |

---

# 🚀 Deployment

The application can be deployed on:

- Render
- Railway
- Fly.io
- Azure App Service
- AWS EC2
- DigitalOcean
- Docker
- Kubernetes

For production deployment, use:

```bash
gunicorn -k uvicorn.workers.UvicornWorker app.main:app
```

instead of development mode (`--reload`).

---

# 📈 Future Improvements

- Docker support
- GitHub Actions CI/CD
- User authentication
- Prediction history
- Model monitoring
- Explainable AI (SHAP)
- Database integration
- User dashboard
- Rate limiting
- Unit and integration tests

---

# 📸 Screenshots

Add screenshots here after deployment.

### Home Page

```
images/home.png
```

### Prediction Results

```
images/result.png
```

### Swagger Documentation

```
images/swagger.png
```

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit changes

```bash
git commit -m "Add new feature"
```

4. Push

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Nour Atef Shehata Farag El-Hadidy**

Computer Engineering Student — Egypt-Japan University of Science and Technology (E-JUST)

AI Researcher | Full-Stack Developer | Machine Learning Engineer

GitHub: https://github.com/nourshehata183

LinkedIn: *(Add your LinkedIn URL)*

---

## ⭐ Support

If you found this project useful, consider giving it a **star** on GitHub. It helps others discover the project and supports future development.

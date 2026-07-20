# Diabetes Risk Prediction — FastAPI

A FastAPI conversion of the original two Streamlit apps. Same models,
same feature engineering, now served as a proper backend with a JSON API,
auto-generated docs, and a small HTML/JS frontend.

## Project structure

```
diabetes-fastapi/
├── app/
│   ├── main.py              # FastAPI app, mounts routers + static files
│   ├── config.py            # File paths & constants
│   ├── models/
│   │   └── schemas.py       # Pydantic request/response models (replaces st widgets)
│   ├── services/
│   │   └── prediction.py    # ML loading + inference logic (replaces script body)
│   ├── routers/
│   │   ├── predict.py       # POST /api/predict/v1, /v2  (JSON API)
│   │   └── pages.py         # GET /  (HTML page)
│   ├── templates/
│   │   └── index.html       # Frontend form (Jinja2)
│   └── static/
│       ├── style.css
│       └── app.js           # fetch() calls to the API
├── ml_models/                # <- put your .pkl files here (see README inside)
├── requirements.txt
├── run.py
└── README.md
```

## Why this structure

- **`services/`** holds all the ML logic that used to be tangled with
  `st.slider(...)` calls in your scripts. It's plain Python — testable,
  reusable, and has nothing to do with HTTP.
- **`schemas.py`** replaces manual input widgets with Pydantic validation.
  Bad input (e.g. `age=500`) is rejected automatically with a 422 error,
  and the same schema powers the interactive docs at `/docs`.
- **`routers/`** are thin — they just call the service and translate
  errors into HTTP responses. No business logic lives here.
- Models load **once at startup** (module-level singletons in
  `prediction.py`), not on every request — the biggest performance
  difference vs. the Streamlit script re-running top to bottom.

## Setup

```bash
cd diabetes-fastapi
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy your `.pkl` files into `ml_models/` (see `ml_models/README.md` for
exact filenames expected by each model version).

## Run

```bash
python run.py
# or
uvicorn app.main:app --reload
```

- Web UI: http://127.0.0.1:8000/
- Interactive API docs (Swagger): http://127.0.0.1:8000/docs
- Alternative docs (ReDoc): http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health
- Model load status: http://127.0.0.1:8000/api/predict/status

## API

### `POST /api/predict/v1`
Clean production model (`xgb_diabetes_model6.pkl`).

```bash
curl -X POST http://127.0.0.1:8000/api/predict/v1 \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45, "bmi": 27.5, "hypertension": 0, "heart_disease": 0,
    "smoking_history": 0, "hba1c_level": 5.6,
    "blood_glucose_level": 110, "gender": 0
  }'
```

### `POST /api/predict/v2`
Backend-aligned pipeline model (`diabetes_pipeline(1).pkl`), full raw
feature set including duplicated columns from the original training data.

```bash
curl -X POST http://127.0.0.1:8000/api/predict/v2 \
  -H "Content-Type: application/json" \
  -d '{
    "AGE": 45, "age": 45, "BMI": 28.5, "bmi": 28.5,
    "blood_glucose_level": 110, "HbA1c_level": 5.7, "HbA1c": 5.7,
    "Cr": 1.0, "TG": 150, "LDL": 100, "HDL": 50, "Chol": 200,
    "Urea": 30, "VLDL": 20, "ID": 1, "No_Pation": 1, "CLASS": 0,
    "smoking_history": 0, "heart_disease": 0, "hypertension": 0,
    "Gender": 0, "gender": 0
  }'
```

Both return:
```json
{
  "probability": 0.1234,
  "prediction": 0,
  "risk_label": "Low Risk of Diabetes",
  "threshold_used": 0.5,
  "model_version": "v1-xgb-model6"
}
```

## Notes / things worth revisiting

- **Model v2's duplicate columns** (`age`/`AGE`, `bmi`/`BMI`,
  `gender`/`Gender`, `HbA1c_level`/`HbA1c`) were preserved as-is from your
  original pipeline so predictions stay identical. Worth cleaning up the
  training data later so the API doesn't need to ask for the same value
  twice.
- **`ID` / `No_Pation` / `CLASS` as model inputs** in v2 look like
  identifier/leakage columns from the source dataset rather than real
  predictive features — flagging in case that pipeline should be
  retrained without them.
- Deploy behind a real ASGI server (e.g. `uvicorn` with `gunicorn` workers,
  or a platform like Render/Fly.io/Azure App Service) rather than
  `--reload` mode.
- Add CORS middleware in `app/main.py` if the frontend will ever be
  hosted on a different origin than the API.

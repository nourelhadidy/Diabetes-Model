"""
Central configuration for the app.

Keeping file paths and constants here means the rest of the code never
hardcodes strings, and you can override paths via environment variables
without touching any logic.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ML_MODELS_DIR = Path(os.getenv("ML_MODELS_DIR", BASE_DIR / "ml_models"))

# --- Model v1 (clean/production model) artifact paths ---
V1_MODEL_PATH = ML_MODELS_DIR / "xgb_diabetes_model6.pkl"
V1_SCALER_PATH = ML_MODELS_DIR / "scaler6.pkl"
V1_SELECTOR_PATH = ML_MODELS_DIR / "selector6.pkl"
V1_FEATURE_NAMES_PATH = ML_MODELS_DIR / "selected_feature_names6.pkl"

# --- Model v2 (backend-aligned pipeline) artifact paths ---
V2_PIPELINE_PATH = ML_MODELS_DIR / "diabetes_pipeline(1).pkl"
V2_THRESHOLD_PATH = ML_MODELS_DIR / "best_threshold(2).pkl"

APP_TITLE = "Diabetes Risk Prediction API"
APP_VERSION = "1.0.0"

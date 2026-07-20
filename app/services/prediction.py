"""
Prediction service.

This is where your original Streamlit "load model -> build feature dict ->
transform -> predict" logic lives now. It's isolated from the web layer
(routers) so it can be unit-tested or reused (CLI, batch jobs, etc.)
without spinning up FastAPI at all.

Models are loaded once at import time (module-level singletons), not on
every request — loading a pickle per-request is the #1 latency killer
people carry over from Streamlit scripts.
"""
import logging

import joblib
import pandas as pd

from app.config import (
    V1_MODEL_PATH,
    V1_SCALER_PATH,
    V1_SELECTOR_PATH,
    V1_FEATURE_NAMES_PATH,
    V2_PIPELINE_PATH,
    V2_THRESHOLD_PATH,
)
from app.models.schemas import DiabetesInputV1, DiabetesInputV2, PredictionResponse

logger = logging.getLogger(__name__)


class ModelNotLoadedError(RuntimeError):
    """Raised when a prediction is requested but the artifact failed to load."""


class DiabetesPredictorV1:
    """Wraps xgb_diabetes_model6.pkl + scaler6.pkl + selector6.pkl."""

    def __init__(self) -> None:
        self.model = None
        self.scaler = None
        self.selector = None
        self.feature_names = None
        self._load()

    def _load(self) -> None:
        try:
            self.model = joblib.load(V1_MODEL_PATH)
            self.scaler = joblib.load(V1_SCALER_PATH)
            self.selector = joblib.load(V1_SELECTOR_PATH)
            self.feature_names = joblib.load(V1_FEATURE_NAMES_PATH)
            logger.info("Model v1 artifacts loaded successfully.")
        except FileNotFoundError as exc:
            logger.warning("Model v1 artifacts not found: %s", exc)

    @property
    def is_ready(self) -> bool:
        return all([self.model, self.scaler, self.selector])

    def predict(self, payload: DiabetesInputV1) -> PredictionResponse:
        if not self.is_ready:
            raise ModelNotLoadedError(
                "Model v1 artifacts are missing. Place them in ml_models/."
            )

        smoking_encoded = int(payload.smoking_history)
        gender_encoded = int(payload.gender)

        input_dict = {
            "age": payload.age,
            "bmi": payload.bmi,
            "hypertension": payload.hypertension,
            "heart_disease": payload.heart_disease,
            "smoking_history": smoking_encoded,
            "HbA1c_level": payload.hba1c_level,
            "blood_glucose_level": payload.blood_glucose_level,
            "gender": gender_encoded,
            "bmi_age": payload.bmi * payload.age,
            "bp_bmi": payload.hypertension * payload.bmi,
            "heart_smoke": payload.heart_disease * smoking_encoded,
        }

        input_df = pd.DataFrame([input_dict])
        x_selected = self.selector.transform(input_df)
        x_scaled = self.scaler.transform(x_selected)

        proba = float(self.model.predict_proba(x_scaled)[0, 1])
        prediction = int(proba > 0.5)

        return PredictionResponse(
            probability=proba,
            prediction=prediction,
            risk_label="High Risk of Diabetes" if prediction == 1 else "Low Risk of Diabetes",
            threshold_used=0.5,
            model_version="v1-xgb-model6",
        )


class DiabetesPredictorV2:
    """Wraps diabetes_pipeline(1).pkl + best_threshold(2).pkl."""

    FULL_FEATURES = [
        "Cr", "AGE", "CLASS", "smoking_history", "ID", "TG", "Gender", "LDL",
        "heart_disease", "gender", "No_Pation", "bmi", "blood_glucose_level",
        "HbA1c_level", "BMI", "Chol", "Urea", "VLDL", "HbA1c", "HDL", "age",
        "hypertension", "bmi_age", "bp_bmi", "heart_smoke",
    ]

    def __init__(self) -> None:
        self.pipeline = None
        self.threshold = 0.5
        self._load()

    def _load(self) -> None:
        try:
            self.pipeline = joblib.load(V2_PIPELINE_PATH)
            self.threshold = joblib.load(V2_THRESHOLD_PATH)
            logger.info("Model v2 artifacts loaded successfully.")
        except FileNotFoundError as exc:
            logger.warning("Model v2 artifacts not found: %s", exc)

    @property
    def is_ready(self) -> bool:
        return self.pipeline is not None

    def predict(self, payload: DiabetesInputV2) -> PredictionResponse:
        if not self.is_ready:
            raise ModelNotLoadedError(
                "Model v2 artifacts are missing. Place them in ml_models/."
            )

        user_input = payload.model_dump()
        # Pydantic gives us IntEnum members for smoking_history/Gender/gender;
        # coerce to plain ints for the dataframe.
        user_input["smoking_history"] = int(payload.smoking_history)
        user_input["Gender"] = int(payload.Gender)
        user_input["gender"] = int(payload.gender)

        user_input["bmi_age"] = user_input["bmi"] * user_input["age"]
        user_input["bp_bmi"] = user_input["hypertension"] * user_input["bmi"]
        user_input["heart_smoke"] = user_input["heart_disease"] * user_input["smoking_history"]

        row = [user_input.get(col, 0) for col in self.FULL_FEATURES]
        df = pd.DataFrame([row], columns=self.FULL_FEATURES)

        proba = float(self.pipeline.predict_proba(df)[:, 1][0])
        prediction = int(proba > self.threshold)

        return PredictionResponse(
            probability=proba,
            prediction=prediction,
            risk_label="High Risk of Diabetes" if prediction == 1 else "Low Risk of Diabetes",
            threshold_used=float(self.threshold),
            model_version="v2-pipeline-backend-aligned",
        )


# Module-level singletons — loaded once when the app starts.
predictor_v1 = DiabetesPredictorV1()
predictor_v2 = DiabetesPredictorV2()

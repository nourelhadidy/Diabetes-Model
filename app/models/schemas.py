"""
Pydantic schemas — these replace the manual `st.slider` / `st.selectbox`
input widgets with validated request bodies. FastAPI uses these to
auto-generate docs (/docs) and to reject bad input before it ever reaches
the model.
"""
from enum import IntEnum
from pydantic import BaseModel, Field


class Gender(IntEnum):
    male = 0
    female = 1
    other = 2


class SmokingHistory(IntEnum):
    never = 0
    current = 1
    former = 2
    ever = 3
    not_current = 4
    no_info = 5


# ---------------------------------------------------------------------
# Model v1 — clean production input (matches xgb_diabetes_model6.pkl)
# ---------------------------------------------------------------------
class DiabetesInputV1(BaseModel):
    age: int = Field(..., ge=1, le=120, description="Age in years")
    bmi: float = Field(..., ge=10.0, le=60.0, description="Body Mass Index")
    hypertension: int = Field(..., ge=0, le=1, description="0 = No, 1 = Yes")
    heart_disease: int = Field(..., ge=0, le=1, description="0 = No, 1 = Yes")
    smoking_history: SmokingHistory = Field(..., description="Smoking history category")
    hba1c_level: float = Field(..., ge=3.0, le=15.0, description="HbA1c level")
    blood_glucose_level: float = Field(..., ge=50.0, le=300.0, description="Blood glucose (mg/dL)")
    gender: Gender = Field(..., description="Gender")

    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 45,
                "bmi": 27.5,
                "hypertension": 0,
                "heart_disease": 0,
                "smoking_history": 0,
                "hba1c_level": 5.6,
                "blood_glucose_level": 110,
                "gender": 0,
            }
        }
    }


# ---------------------------------------------------------------------
# Model v2 — backend-aligned pipeline input (matches diabetes_pipeline(1).pkl)
# This mirrors every raw column the pipeline was trained on, including
# the duplicated upper/lowercase fields from the original notebook.
# ---------------------------------------------------------------------
class DiabetesInputV2(BaseModel):
    AGE: int = Field(..., ge=1, le=120)
    age: int = Field(..., ge=1, le=120)
    BMI: float = Field(..., ge=10.0, le=60.0)
    bmi: float = Field(..., ge=10.0, le=60.0)
    blood_glucose_level: float = Field(..., ge=50.0, le=300.0)
    HbA1c_level: float = Field(..., ge=3.0, le=15.0)
    HbA1c: float = Field(..., ge=3.0, le=15.0)
    Cr: float = Field(..., ge=0.1, le=20.0, description="Creatinine")
    TG: float = Field(..., ge=30.0, le=1000.0, description="Triglycerides")
    LDL: float = Field(..., ge=10.0, le=300.0)
    HDL: float = Field(..., ge=10.0, le=150.0)
    Chol: float = Field(..., ge=50.0, le=400.0, description="Cholesterol")
    Urea: float = Field(..., ge=5.0, le=150.0)
    VLDL: float = Field(..., ge=5.0, le=100.0)
    ID: int = Field(0, ge=0, le=999999)
    No_Pation: int = Field(0, ge=0, le=999999)
    CLASS: int = Field(0, ge=0, le=10)
    smoking_history: SmokingHistory
    heart_disease: int = Field(..., ge=0, le=1)
    hypertension: int = Field(..., ge=0, le=1)
    Gender: Gender
    gender: Gender

    model_config = {
        "json_schema_extra": {
            "example": {
                "AGE": 45, "age": 45,
                "BMI": 28.5, "bmi": 28.5,
                "blood_glucose_level": 110,
                "HbA1c_level": 5.7, "HbA1c": 5.7,
                "Cr": 1.0, "TG": 150, "LDL": 100, "HDL": 50,
                "Chol": 200, "Urea": 30, "VLDL": 20,
                "ID": 1, "No_Pation": 1, "CLASS": 0,
                "smoking_history": 0, "heart_disease": 0, "hypertension": 0,
                "Gender": 0, "gender": 0,
            }
        }
    }


# ---------------------------------------------------------------------
# Shared response schema
# ---------------------------------------------------------------------
class PredictionResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    probability: float = Field(..., description="Predicted probability of diabetes risk (0-1)")
    prediction: int = Field(..., description="0 = Low risk, 1 = High risk")
    risk_label: str
    threshold_used: float
    model_version: str

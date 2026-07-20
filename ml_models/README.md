# Model artifacts go here

Copy your existing `.pkl` files from the Streamlit project into this folder,
keeping the exact filenames:

For **Model v1** (`/api/predict/v1`):
- `xgb_diabetes_model6.pkl`
- `scaler6.pkl`
- `selector6.pkl`
- `selected_feature_names6.pkl`

For **Model v2** (`/api/predict/v2`):
- `diabetes_pipeline(1).pkl`
- `best_threshold(2).pkl`

If a model's files are missing, that endpoint will return `503 Service
Unavailable` instead of crashing the whole app — check `/api/predict/status`
to see which models loaded successfully.

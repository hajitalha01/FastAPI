from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# ============================================================
# 1. APP
# ============================================================

app = FastAPI(
    title="House Price Prediction API",
    description="API for predicting house prices using a Machine Learning model.",
    version="1.0.0",
)


# ============================================================
# 2. CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production mein apna frontend URL dena
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 3. MODEL PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml" / "house_price_model.pkl"


# ============================================================
# 4. LOAD MODEL
# ============================================================

try:
    saved_data = joblib.load(MODEL_PATH)

    model = saved_data["model"]
    locations = saved_data["locations"]

    print("Model loaded successfully.")
    print("Model type:", type(model))
    print("Locations:", locations)

except FileNotFoundError:
    model = None
    locations = []
    print(f"Model file not found: {MODEL_PATH}")

except Exception as e:
    model = None
    locations = []
    print(f"Error loading model: {e}")

# ============================================================
# 5. REQUEST SCHEMA
# ============================================================

class HouseData(BaseModel):
    bedrooms: int = Field(..., ge=1, le=20)
    bathrooms: int = Field(..., ge=1, le=20)
    kitchens: int = Field(..., ge=1, le=10)
    tv_lounges: int = Field(..., ge=0, le=10)
    area_sqm: float = Field(..., gt=0)
    location: str = Field(..., min_length=2, max_length=100)


# ============================================================
# 6. RESPONSE / ROOT
# ============================================================

@app.get("/")
def home():
    return {
        "message": "House Price Prediction API is running",
        "docs": "/docs",
    }


# ============================================================
# 7. HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": model is not None,
    }


# ============================================================
# 8. PREDICTION ENDPOINT
# ============================================================

@app.post("/predict")
def predict_house_price(data: HouseData):

    if model is None:
        raise HTTPException(
            status_code=500,
            detail="ML model is not loaded.",
        )

    try:
        # DataFrame exactly model ke features ke naam ke saath
        input_data = pd.DataFrame(
            [
                {
                    "bedrooms": data.bedrooms,
                    "bathrooms": data.bathrooms,
                    "kitchens": data.kitchens,
                    "tv_lounges": data.tv_lounges,
                    "area_sqm": data.area_sqm,
                    "location": data.location,
                }
            ]
        )

        # Prediction
        prediction = model.predict(input_data)

        predicted_price = float(prediction[0])

        return {
            "success": True,
            "prediction": {
                "price": round(predicted_price, 2),
                "currency": "PKR",
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}",
        )

from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()


# =========================
# Pydantic Patient Model
# =========================

class Patient(BaseModel):

    id: Annotated[
        str,
        Field(..., description="ID of the patient", examples=["p001"])
    ]

    name: Annotated[
        str,
        Field(..., description="Name of the patient")
    ]

    city: Annotated[
        str,
        Field(..., description="City where the patient lives")
    ]

    age: Annotated[
        int,
        Field(..., gt=0, lt=120, description="Age of the patient")
    ]

    gender: Annotated[
        Literal["male", "female", "other"],
        Field(..., description="Gender of the patient")
    ]

    height: Annotated[
        float,
        Field(..., gt=0, description="Height in meters")
    ]

    weight: Annotated[
        float,
        Field(..., gt=0, description="Weight in kg")
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return "underweight"

        elif self.bmi < 25:
            return "normal"

        elif self.bmi < 30:
            return "overweight"

        else:
            return "obese"


# =========================
# Load Data
# =========================

def load_data():

    with open("patients.json", "r") as f:
        data = json.load(f)

    return data


# =========================
# Save Data
# =========================

def save_data(data):

    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)


# =========================
# Home
# =========================

@app.get("/")
def home():
    return {
        "message": "Patient Management API"
    }


# =========================
# About
# =========================

@app.get("/about")
def about():
    return {
        "message": "This API manages patient records"
    }


# =========================
# View All Patients
# =========================

@app.get("/view")
def view():

    data = load_data()

    return data


# =========================
# View Single Patient
# =========================

@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ...,
        description="ID of the patient",
        examples=["p001"]
    )
):

    data = load_data()

    for patient in data:

        if patient["patient_id"] == patient_id:
            return patient

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )


# =========================
# Sort Patients
# =========================

@app.get("/sort")
def sort_patients(

    sort_by: str = Query(
        ...,
        description="Sort by height, weight or bmi"
    ),

    order: str = Query(
        "asc",
        description="Sort in asc or desc order"
    )
):

    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:

        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Select from {valid_fields}"
        )

    if order not in ["asc", "desc"]:

        raise HTTPException(
            status_code=400,
            detail="Invalid order. Select from asc or desc"
        )

    data = load_data()

    sort_order = True if order == "desc" else False

    sorted_data = sorted(
        data,
        key=lambda x: x.get(sort_by, 0),
        reverse=sort_order
    )

    return sorted_data


# =========================
# Create New Patient
# =========================

@app.post("/create", status_code=201)
def create_patient(patient: Patient):

    data = load_data()

    # Check duplicate patient ID
    for existing_patient in data:

        if existing_patient["patient_id"] == patient.id:

            raise HTTPException(
                status_code=400,
                detail="Patient already exists"
            )

    # Convert Pydantic model to dictionary
    new_patient = patient.model_dump()

    # id ko patient_id mein convert karna
    new_patient["patient_id"] = new_patient.pop("id")

    # New patient add karna
    data.append(new_patient)

    # Data save karna
    save_data(data)

    return {
        "message": "Patient created successfully",
        "patient": new_patient
    }
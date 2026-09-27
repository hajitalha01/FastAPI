from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
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
        return round(self.weight / (self.height ** 2), 2)

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
# Pydantic Update Patient Model
# =========================

class PatientUpdate(BaseModel):

    name: Annotated[
        Optional[str],
        Field(default=None)
    ]

    city: Annotated[
        Optional[str],
        Field(default=None)
    ]

    age: Annotated[
        Optional[int],
        Field(default=None, gt=0, lt=120)
    ]

    gender: Annotated[
        Optional[Literal["male", "female", "other"]],
        Field(default=None)
    ]

    height: Annotated[
        Optional[float],
        Field(default=None, gt=0)
    ]

    weight: Annotated[
        Optional[float],
        Field(default=None, gt=0)
    ]


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

    # Save data
    save_data(data)

    return {
        "message": "Patient created successfully",
        "patient": new_patient
    }


# =========================
# Update Patient
# =========================

@app.put("/edit/{patient_id}")
def update_patient(
    patient_id: str,
    patient_update: PatientUpdate
):

    data = load_data()

    # Find patient
    for patient in data:

        if patient["patient_id"] == patient_id:

            # Sirf woh fields update hongi
            # jo request mein di gayi hain
            update_data = patient_update.model_dump(
                exclude_unset=True
            )

            # Update fields
            for key, value in update_data.items():

                if value is not None:
                    patient[key] = value

            # BMI dobara calculate karna
            patient["bmi"] = round(
                patient["weight"] / (patient["height"] ** 2),
                2
            )

            # Verdict dobara calculate karna
            if patient["bmi"] < 18.5:
                patient["verdict"] = "underweight"

            elif patient["bmi"] < 25:
                patient["verdict"] = "normal"

            elif patient["bmi"] < 30:
                patient["verdict"] = "overweight"

            else:
                patient["verdict"] = "obese"

            # Save updated data
            save_data(data)

            return {
                "message": "Patient updated successfully",
                "patient": patient
            }

    # Patient nahi mila
    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )
# =========================
# Delete Patient
# =========================

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):

    data = load_data()

    # Patient find karo
    for index, patient in enumerate(data):

        if patient["patient_id"] == patient_id:

            # Patient ko list se remove karo
            deleted_patient = data.pop(index)

            # Updated data save karo
            save_data(data)

            return {
                "message": "Patient deleted successfully",
                "patient": deleted_patient
            }

    # Patient nahi mila
    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )
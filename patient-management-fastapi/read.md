# Patient Management API

A simple Patient Management REST API built with **FastAPI**, **Pydantic**, and **JSON**.

This project is part of my FastAPI learning journey. It currently implements complete **CRUD operations** for managing patient records.

---

## 🚀 Features

- Create a new patient
- View all patients
- View a single patient by ID
- Update patient information
- Delete a patient
- Sort patients by height, weight, or BMI
- Automatic BMI calculation
- Automatic BMI verdict
- Pydantic data validation
- Swagger API documentation

---

## 🛠️ Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- JSON
- Git & GitHub

---

## 📁 Project Structure

```text
patient-management-fastapi/
│
├── main.py
├── patients.json
└── README.md
⚙️ Installation

First, create a virtual environment:

python -m venv venv

Activate the virtual environment.

Windows PowerShell
venv\Scripts\Activate.ps1

Install the required packages:

pip install fastapi uvicorn pydantic
▶️ Run the API

Run the FastAPI application with:

uvicorn main:app --reload

The API will run at:

http://127.0.0.1:8000
📚 API Documentation

FastAPI automatically provides Swagger documentation.

Open:

http://127.0.0.1:8000/docs

Alternative documentation:

http://127.0.0.1:8000/redoc

🔥 API Endpoints
1. Home
GET /

Returns a simple welcome message.

Example response:

{
  "message": "Patient Management API"
}
2. About
GET /about

Returns information about the API.

Example response:

{
  "message": "This API manages patient records"
}
3. View All Patients
GET /view

Returns all patients stored in patients.json.

Example:

GET http://127.0.0.1:8000/view
4. View Single Patient
GET /patient/{patient_id}

Returns a patient using their patient ID.

Example:

GET /patient/p001

Example response:

{
  "patient_id": "p001",
  "name": "Ali",
  "age": 22,
  "gender": "male",
  "height": 1.75,
  "weight": 70,
  "city": "Rawalpindi",
  "bmi": 22.86,
  "verdict": "normal"
}

If the patient does not exist:

{
  "detail": "Patient not found"
}
5. Create Patient
POST /create

Creates a new patient.

Example request:

{
  "id": "p006",
  "name": "Hassan",
  "city": "Peshawar",
  "age": 26,
  "gender": "male",
  "height": 1.75,
  "weight": 72
}

The API automatically calculates:

BMI
BMI verdict

Example response:

{
  "message": "Patient created successfully",
  "patient": {
    "name": "Hassan",
    "city": "Peshawar",
    "age": 26,
    "gender": "male",
    "height": 1.75,
    "weight": 72,
    "bmi": 23.51,
    "verdict": "normal",
    "patient_id": "p006"
  }
}
6. Update Patient
PUT /edit/{patient_id}

Updates an existing patient.

Example:

PUT /edit/p001

Request body:

{
  "weight": 75
}

You can update multiple fields:

{
  "name": "Ali Khan",
  "city": "Lahore",
  "age": 25,
  "weight": 75
}

After updating the weight or height, BMI and verdict are recalculated automatically.

Example response:

{
  "message": "Patient updated successfully",
  "patient": {
    "patient_id": "p001",
    "name": "Ali Khan",
    "city": "Lahore",
    "age": 25,
    "gender": "male",
    "height": 1.75,
    "weight": 75,
    "bmi": 24.49,
    "verdict": "normal"
  }
}
7. Delete Patient
DELETE /delete/{patient_id}

Deletes a patient from the database.

Example:

DELETE /delete/p006

Example response:

{
  "message": "Patient deleted successfully",
  "patient": {
    "patient_id": "p006",
    "name": "Hassan"
  }
}

If the patient does not exist:

{
  "detail": "Patient not found"
}
8. Sort Patients
GET /sort

Patients can be sorted by:

height
weight
BMI
Sort by height
/sort?sort_by=height&order=asc
Sort by weight
/sort?sort_by=weight&order=desc
Sort by BMI
/sort?sort_by=bmi&order=asc

Supported orders:

asc
desc
🧮 BMI Calculation

BMI is calculated using:

BMI = weight / (height²)

Where:

Weight is in kilograms
Height is in meters

Example:

Weight = 70 kg
Height = 1.75 m

BMI = 70 / (1.75 × 1.75)
BMI = 22.86
📊 BMI Verdict

The API automatically generates a verdict based on BMI:

BMI	Verdict
Below 18.5	Underweight
18.5 - 24.99	Normal
25 - 29.99	Overweight
30 or above	Obese
🛡️ Data Validation

Pydantic is used for validating patient data.

For example:

Age must be greater than 0
Age must be less than 120
Height must be greater than 0
Weight must be greater than 0
Gender must be male, female, or other

Invalid data will automatically generate a validation error from FastAPI.

🗄️ Database

This project currently uses a JSON file instead of a traditional database.

Patient data is stored in:

patients.json

The application uses Python's json module to:

Read patient data
Add new patients
Update patients
Delete patients
Save updated data
🔄 CRUD Operations

This project implements complete CRUD functionality.

Operation	HTTP Method	Endpoint
Create	POST	/create
Read All	GET	/view
Read One	GET	/patient/{patient_id}
Update	PUT	/edit/{patient_id}
Delete	DELETE	/delete/{patient_id}
🧪 Testing

The API can be tested using:

Swagger UI
Postman
Browser for GET requests
Any REST API client

Swagger:

http://127.0.0.1:8000/docs
📌 Current Project Status
Completed
 FastAPI setup
 Pydantic Patient Model
 Patient validation
 Create patient
 Read all patients
 Read single patient
 Update patient
 Delete patient
 Sort patients
 Automatic BMI calculation
 Automatic BMI verdict
 Error handling
 Swagger documentation
 JSON file storage
🚀 Future Improvements

Possible future improvements:

Add a real database such as PostgreSQL or SQLite
Add SQLAlchemy
Add authentication and authorization
Add pagination
Add search functionality
Add filtering
Add automated tests with Pytest
Add Docker support
Deploy the API online
👨‍💻 Author

Haji Talha

This project is part of my journey of learning FastAPI and Backend Development with Python.

⭐ Repository

This project is part of my FastAPI repository where I will continue adding more API projects.

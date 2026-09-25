from fastapi import FastAPI
import json

app = FastAPI()


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)

    return data


@app.get("/")
def home():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message": "A Fully Functional API to Manage Your Patient Records"}


@app.get("/view")
def view():
    data = load_data()
    return data

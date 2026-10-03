# House Price Prediction API

A machine learning based House Price Prediction project built with **Python, Scikit-learn, FastAPI, Streamlit, and Docker**.

The project predicts house prices based on property features such as bedrooms, bathrooms, kitchens, TV lounges, area, and location.

---

## 🚀 Features

* Machine Learning house price prediction
* FastAPI REST API
* Streamlit web interface
* Input validation using Pydantic
* Location-based prediction
* Health check endpoint
* Swagger API documentation
* Dockerized application
* Docker Hub image available
* FastAPI and Streamlit running inside Docker container

---

## 🛠️ Technologies Used

* Python 3.11
* Pandas
* Scikit-learn
* Joblib
* FastAPI
* Uvicorn
* Pydantic
* Streamlit
* Requests
* Docker
* Docker Hub

---

## 📁 Project Structure

```text
FastAPi/
│
├── README.md
├── requirements.txt
├── Dockerfile
├── .dockerignore
│
├── api/
│   └── api.py
│
├── frontend/
│   └── streamlit_app.py
│
└── ml/
    ├── house_data.csv
    ├── house_price_model.pkl
    └── train_model.py
```

---

## 🤖 Machine Learning Model

The trained model is stored in:

```text
ml/house_price_model.pkl
```

The saved model contains:

* Trained Scikit-learn pipeline
* Available house locations

The model predicts the estimated house price in **PKR**.

---

## 📊 Input Features

The prediction system accepts the following inputs:

| Feature    | Description                    |
| ---------- | ------------------------------ |
| Bedrooms   | Number of bedrooms             |
| Bathrooms  | Number of bathrooms            |
| Kitchens   | Number of kitchens             |
| TV Lounges | Number of TV lounges           |
| Area       | Property area in square meters |
| Location   | Property location              |

### Available Locations

The model contains locations including:

* Bahria Town Rawalpindi
* Clifton Karachi
* DHA Islamabad
* DHA Lahore
* F-10 Islamabad
* Gulberg Lahore
* Gulshan-e-Iqbal Karachi
* Hayatabad Peshawar
* Johar Town Lahore
* Saddar Rawalpindi
* Satellite Town Rawalpindi

---

# ⚙️ Run Locally

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required Python libraries.

---

## 2. Run FastAPI

```bash
python -m uvicorn api.api:app --reload
```

FastAPI will run at:

```text
http://127.0.0.1:8000
```

### Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger provides an interactive interface for testing the API.

### Health Check

Open:

```text
http://127.0.0.1:8000/health
```

---

## 3. Run Streamlit

Open another terminal and run:

```bash
python -m streamlit run frontend/streamlit_app.py
```

Streamlit will normally be available at:

```text
http://localhost:8501
```

---

# 🐳 Docker

The complete application has been Dockerized.

The Docker container runs:

* FastAPI backend on port `8000`
* Streamlit frontend on port `8501`

---

## Dockerfile

The project uses Python 3.11 Slim as the base image.

The Docker image installs the required dependencies and copies the complete project into the container.

---

## Build Docker Image

From the project root directory:

```bash
docker build -t house-price-predictor .
```

This command builds the Docker image using the `Dockerfile`.

---

## Run Docker Container

```bash
docker run -d --name house-price-app -p 8000:8000 -p 8501:8501 house-price-predictor
```

This command:

* Creates a container named `house-price-app`
* Runs it in detached/background mode
* Maps FastAPI port `8000`
* Maps Streamlit port `8501`

---

## Check Running Container

```bash
docker ps
```

This displays currently running Docker containers.

---

## Docker Application URLs

### FastAPI

```text
http://localhost:8000
```

### FastAPI Swagger

```text
http://localhost:8000/docs
```

### FastAPI Health Check

```text
http://localhost:8000/health
```

### Streamlit

```text
http://localhost:8501
```

---

# 🐳 Docker Hub

The Docker image has been published to Docker Hub.

## Docker Hub Repository

**hajitalha/house-price-predictor**

https://hub.docker.com/r/hajitalha/house-price-predictor

---

## Docker Hub Login

```bash
docker login
```

This logs in to Docker Hub.

---

## Tag Docker Image

```bash
docker tag house-price-predictor hajitalha/house-price-predictor:latest
```

This gives the local Docker image a Docker Hub repository name.

---

## Push Image to Docker Hub

```bash
docker push hajitalha/house-price-predictor:latest
```

This uploads the Docker image to the Docker Hub repository.

---

## Pull Image from Docker Hub

Anyone with access to the image can download it using:

```bash
docker pull hajitalha/house-price-predictor:latest
```

Then run it with:

```bash
docker run -d --name house-price-app -p 8000:8000 -p 8501:8501 hajitalha/house-price-predictor:latest
```

---

# 🔄 Application Architecture

```text
                    User
                      |
                      v
              Streamlit Frontend
                Port 8501
                      |
                      v
               FastAPI Backend
                Port 8000
                      |
                      v
              ML Prediction Model
                      |
                      v
              Predicted House Price
                    (PKR)
```

### Docker Architecture

```text
             Docker Container
        ┌─────────────────────────┐
        │                         │
        │  Streamlit :8501        │
        │         │               │
        │         v               │
        │  FastAPI :8000          │
        │         │               │
        │         v               │
        │  ML Model               │
        │                         │
        └─────────────────────────┘
```

---

# 🧪 API Prediction Request

The prediction endpoint is:

```text
POST /predict
```

Example request:

```json
{
  "bedrooms": 3,
  "bathrooms": 2,
  "kitchens": 1,
  "tv_lounges": 1,
  "area_sqm": 200,
  "location": "DHA Islamabad"
}
```

Example response:

```json
{
  "success": true,
  "prediction": {
    "price": 25000000.0,
    "currency": "PKR"
  }
}
```

*The example price above is illustrative; actual predictions are generated by the trained model.*

---

# 🔍 Health Check

The `/health` endpoint checks whether the API and machine learning model are available.

Example:

```text
GET /health
```

---

# 📦 Docker Commands Summary

### Build image

```bash
docker build -t house-price-predictor .
```

### Run container

```bash
docker run -d --name house-price-app -p 8000:8000 -p 8501:8501 house-price-predictor
```

### Check containers

```bash
docker ps
```

### View logs

```bash
docker logs house-price-app
```

### Stop container

```bash
docker stop house-price-app
```

### Start existing container

```bash
docker start house-price-app
```

### Tag image

```bash
docker tag house-price-predictor hajitalha/house-price-predictor:latest
```

### Push to Docker Hub

```bash
docker push hajitalha/house-price-predictor:latest
```

### Pull from Docker Hub

```bash
docker pull hajitalha/house-price-predictor:latest
```

---

# 🔮 Future Improvements

* Improve model accuracy with a larger dataset
* Add more property features
* Add authentication for API
* Add database integration
* Deploy to a cloud platform
* Use separate Docker containers for FastAPI and Streamlit
* Add automated CI/CD pipeline

---

# 👨‍💻 Project

**House Price Prediction System**

Built using:

**Machine Learning + FastAPI + Streamlit + Docker + Docker Hub**

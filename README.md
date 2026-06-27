# 🏨 Hotel Reservation Cancellation Prediction

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![LightGBM](https://img.shields.io/badge/Model-LightGBM-success.svg)](https://lightgbm.readthedocs.io/)
[![Flask](https://img.shields.io/badge/API-Flask-black.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED.svg)](https://www.docker.com/)
[![Jenkins](https://img.shields.io/badge/CI%2FCD-Jenkins-D24939.svg)](https://www.jenkins.io/)
[![MLflow](https://img.shields.io/badge/Tracking-MLflow-0194E2.svg)](https://mlflow.org/)
[![Deployed on Render](https://img.shields.io/badge/Deployed-Render-46E3B7.svg)](https://render.com/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20App-brightgreen.svg)](https://hotel-reservation-prediction-ip4v.onrender.com/)

An end-to-end, production-style **Machine Learning system** that predicts whether a hotel booking will be **honored or cancelled**, based on reservation details. The project goes beyond model training — it includes a fully automated **CI/CD pipeline**, **experiment tracking**, **containerized deployment**, and a live **web interface** for real-time predictions.

🔗 **Live App:** [hotel-reservation-prediction-ip4v.onrender.com](https://hotel-reservation-prediction-ip4v.onrender.com/)

---

## 📌 Overview

Hotel cancellations cost the hospitality industry significant revenue every year. This project builds a binary classification model using **LightGBM** to predict cancellation risk from booking attributes (lead time, deposit type, special requests, market segment, etc.), enabling hotels to proactively manage overbooking, staffing, and revenue strategies.

The system is engineered as a complete **MLOps pipeline** — from data ingestion to a live, deployed web app — rather than a standalone notebook experiment.

---

## ✨ Key Features

- 🔮 **Predictive Modeling** — LightGBM classifier trained on historical reservation data to flag high-risk cancellations.
- ☁️ **Cloud-Native Data Ingestion** — Pulls training data from **Google Cloud Storage**, with an automatic **local fallback** if the cloud bucket is unreachable.
- 📊 **Experiment Tracking** — All training runs, hyperparameters, metrics, and model artifacts are logged via **MLflow**.
- 🔁 **Automated CI/CD** — **Jenkins** pipeline automatically builds, trains, tests, and deploys on every push to `main`.
- 🐳 **Containerized Deployment** — Packaged into a lightweight **Docker** image for consistent, portable deployment.
- 🌐 **Live Web Interface** — A **Flask**-based API/UI deployed on **Render** for real-time predictions.
- 🛡️ **Resilient Design** — Pipeline is fault-tolerant; a missing cloud connection never breaks the training run.

---

## 🧠 Model Performance

| Metric | Score |
|---|---|
| **Accuracy** | **86.37%** |
| **F1-Score** | **86.77%** |
| Precision | _TBD_ |
| Recall | _TBD_ |
| ROC-AUC | _TBD_ |

> Metrics are logged automatically via MLflow on every training run for full reproducibility and comparison across experiments.

---

## 🏗️ Architecture & Workflow

```
                ┌─────────────┐
                │   GitHub    │
                │  (git push) │
                └──────┬──────┘
                       │ triggers
                       ▼
                ┌─────────────┐
                │   Jenkins   │
                │   Pipeline  │
                └──────┬──────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
   ┌────────────┐ ┌──────────┐ ┌──────────┐
   │  Venv +    │ │ Training │ │  MLflow  │
   │  Deps      │ │ Pipeline │ │ Tracking │
   └────────────┘ └────┬─────┘ └──────────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        ┌──────────┐       ┌─────────────┐
        │   GCS    │       │ Local Data  │
        │ (primary)│       │ (fallback)  │
        └──────────┘       └─────────────┘
                       │
                       ▼
                ┌─────────────┐
                │   Docker    │
                │    Build    │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │   Render    │
                │ (Live App)  │
                └─────────────┘
```

---

## ⚙️ CI/CD Pipeline Workflow

The project utilizes an automated **Jenkins-based pipeline** to ensure continuous integration and deployment. The workflow is as follows:

1. **Code Integration (GitHub)**
   Every `git push` to the `main` branch triggers the Jenkins automation server.

2. **Environment Provisioning**
   Jenkins automatically creates a clean Python virtual environment and installs all project dependencies defined in `setup.py`.

3. **Data Ingestion & Training**
   - The pipeline executes `training_pipeline.py`.
   - It attempts to fetch data from **Google Cloud Storage**.
   - **Resiliency:** If cloud storage is inaccessible, a local fallback mechanism automatically loads the dataset from the repository, ensuring the pipeline never fails due to external dependency issues.

4. **Experiment Tracking (MLflow)**
   The training process is tracked via MLflow, which logs model parameters, performance metrics, and artifacts to a local SQLite database and file system.

5. **Containerization (Docker)**
   Upon successful training, Jenkins invokes the Docker CLI to build a production-ready image, bundling the application, the trained LightGBM model, and necessary system dependencies.

6. **Deployment (Render)**
   The final Docker image is deployed to Render, providing a live, scalable web interface for real-time hotel reservation predictions.

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| ML Algorithm | LightGBM |
| ML Utilities | Scikit-Learn |
| Experiment Tracking | MLflow |
| Web Framework | Flask |
| CI/CD | Jenkins |
| Containerization | Docker |
| Cloud Storage | Google Cloud Storage |
| Deployment Platform | Render |

---

## 📂 Project Structure

> _Replace this with your actual structure — update folder/file names to match your repository exactly._

```
hotel-reservation-prediction/
├── artifacts/
│   ├── raw/                  # Raw ingested data
│   ├── processed/            # Cleaned & feature-engineered data
│   └── models/                # Trained model binaries (.pkl / .txt)
├── config/
│   └── config.yaml            # Paths, GCS bucket info, model params
├── src/
│   ├── data_ingestion.py      # GCS + local fallback logic
│   ├── data_preprocessing.py
│   ├── model_training.py
│   └── logger.py
├── pipeline/
│   └── training_pipeline.py   # Orchestrates the full ML pipeline
├── application.py             # Flask app entry point
├── templates/                 # HTML templates for the web UI
├── static/                    # CSS/JS assets
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── setup.py
└── README.md
```

---

## 🚀 Installation & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/hotel-reservation-prediction.git
cd hotel-reservation-prediction
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -e .
```

### 4. Run the training pipeline
```bash
python pipeline/training_pipeline.py
```

### 5. Launch MLflow UI (optional, for tracking)
```bash
mlflow ui
```

### 6. Run the Flask app locally
```bash
python application.py
```
The app will be available at `http://127.0.0.1:5000`.

---

## 🐳 Running with Docker

```bash
# Build the image
docker build -t hotel-reservation-app .

# Run the container
docker run -p 5000:5000 hotel-reservation-app
```

---

## 🔮 Future Improvements

- Add SHAP-based model explainability to the web UI.
- Expand hyperparameter tuning with Optuna.
- Add automated unit/integration tests to the Jenkins pipeline.
- Set up model drift monitoring in production.

---
pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "project-0495f0cf-4319-450f-a85" 
    }

    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(
                        branches: [[name: '*/main']], 
                        extensions: [], 
                        userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/subh737/Hotel-Reservation-Prediction.git']]
                    )
                }
            }
        }

       stage('Setting up our Virtual Environment and Installing dependencies') {
            steps {
                script {
                    echo 'Setting up our Virtual Environment and Installing dependencies............'
                    sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    
                    # Train the model right here in Jenkins!
                    python pipeline/training_pipeline.py
                    '''
                }
            }
        }

        stage('Building Docker Image Locally') {
            steps {
                script {
                    echo 'Building Docker Image Locally (Cloud Push Disabled).............'
                    sh '''
                    # 1. Build the Docker image locally
                    docker build -t ml-project:latest .

                    # --- CLOUD DEPLOYMENT DISABLED FOR LOCAL RUN ---
                    # gcloud config set project ${GCP_PROJECT}
                    # gcloud auth configure-docker --quiet
                    # docker tag ml-project:latest gcr.io/${GCP_PROJECT}/ml-project:latest
                    # docker push gcr.io/${GCP_PROJECT}/ml-project:latest 
                    '''
                }
            }
        }

        stage('Deploy to Google Cloud Run') {
            steps {
                script {
                    echo 'Deploy to Google Cloud Run skipped for local testing.............'
                    
                    /* --- DEPLOYMENT DISABLED FOR LOCAL RUN ---
                    sh '''
                    gcloud config set project ${GCP_PROJECT}

                    gcloud run deploy ml-project \
                        --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
                        --platform=managed \
                        --region=us-central1 \
                        --allow-unauthenticated
                    '''
                    */
                }
            }
        }
    }
}
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

        stage('Building and Pushing Docker Image to GCR') {
            steps {
                script {
                    echo 'Building and Pushing Docker Image to GCR.............'
                    sh '''
                    # 1. Set the correct GCP project
                    gcloud config set project ${GCP_PROJECT}

                    # 2. Tell Docker to use gcloud for authentication
                    gcloud auth configure-docker --quiet

                    # 3. Build the Docker image
                    docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                    # 4. Push the image to Google Container Registry
                    docker push gcr.io/${GCP_PROJECT}/ml-project:latest 
                    '''
                }
            }
        }

        stage('Deploy to Google Cloud Run') {
            steps {
                script {
                    echo 'Deploy to Google Cloud Run.............'
                    sh '''
                    # 1. Ensure the project is set
                    gcloud config set project ${GCP_PROJECT}

                    # 2. Deploy directly to Cloud Run
                    gcloud run deploy ml-project \
                        --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
                        --platform=managed \
                        --region=us-central1 \
                        --allow-unauthenticated
                    '''
                }
            }
        }
    }
}
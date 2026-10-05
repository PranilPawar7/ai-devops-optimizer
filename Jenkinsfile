pipeline {
    agent any

    environment {
        PATH = "C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python312;C:\\Users\\Admin\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;${env.PATH}"
    }

    stages {

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t ai-devops-app .'
            }
        }

        stage('Deploy Container') {
            steps {
                bat 'docker rm -f ai-devops-container || exit /b 0'
                bat 'docker run -d -p 5000:5000 --name ai-devops-container ai-devops-app'
            }
        }
    }
}



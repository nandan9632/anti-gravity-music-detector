pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS = credentials('dockerhub')
        IMAGE_NAME = "nandan/anti-gravity-music"
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/nandan9632/anti-gravity-music-detector.git'
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Login DockerHub') {
            steps {
                sh 'echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin'
            }
        }

        stage('Push Image') {
            steps {
                sh 'docker push $IMAGE_NAME'
            }
        }
    }
}
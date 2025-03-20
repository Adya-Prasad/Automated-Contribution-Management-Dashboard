pipeline {
    agent any
    triggers {
        cron('H/30 * * * *')
    }
    environment {
        DJANGO_SECRET_KEY = credentials('django-secret-key')
        GITHUB_TOKEN = credentials('github-token')
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Adya-Prasad/Automated-Contribution-Management-Dashboard.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Run Migrations') {
            steps {
                bat 'python manage.py migrate'
            }
        }
        stage('Run Automation') {
            steps {
                bat 'python manage.py runscript automation.scripts.pr_manager'
            }
        }
    }
    post {
        failure {
            echo 'Pipeline failed! Check the logs for details.'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
    }
}
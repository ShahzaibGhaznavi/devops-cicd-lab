
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Python Validation') {
            steps {
                sh '''
                    set -e
                    python3 --version
                    python3 -m py_compile app.py test_app.py
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    set -e
                    python3 -m unittest -v
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'sonar-scanner'

                    withSonarQubeEnv('SonarQube') {
                        sh """
                            '${scannerHome}/bin/sonar-scanner' \
                              -Dsonar.projectKey=devops-cicd-lab \
                              -Dsonar.projectName=devops-cicd-lab \
                              -Dsonar.sources=. \
                              -Dsonar.scm.disabled=true
                        """
                    }
                }
            }
        }
    }
}

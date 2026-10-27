
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=devops-cicd-lab \
                          -Dsonar.projectName=devops-cicd-lab \
                          -Dsonar.sources=. \
                          -Dsonar.scm.disabled=true
                    '''
                }
            }
        }
    }
}

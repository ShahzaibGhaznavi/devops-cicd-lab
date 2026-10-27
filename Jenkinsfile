
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

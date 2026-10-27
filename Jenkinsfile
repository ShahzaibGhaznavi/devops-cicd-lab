
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

        stage('Trivy Filesystem Scan') {
            steps {
                sh '''
                    set +e
                    trivy --config /dev/null fs \
                      --scanners vuln,misconfig,secret \
                      --format table \
                      --output trivy-report.txt \
                      .
                    scan_status=$?
                    set -e

                    cat trivy-report.txt

                    if [ "$scan_status" -ne 0 ]; then
                        echo "Trivy scanner failed to complete."
                        exit "$scan_status"
                    fi
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-report.txt',
                                     allowEmptyArchive: true
                }
            }
        }


        stage('Docker Build') {
            steps {
                sh '''
                    set -e
                    docker build -t devops-cicd-lab:${BUILD_NUMBER} .
                    docker tag devops-cicd-lab:${BUILD_NUMBER} devops-cicd-lab:latest
                '''
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh '''
                    set -e
                    trivy --config /dev/null image \
                      --scanners vuln,secret \
                      --format table \
                      devops-cicd-lab:${BUILD_NUMBER}
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
                              -Dsonar.python.version=3.12 \
                              -Dsonar.scm.disabled=true
                        """
                    }
                }
            }
        }
    }
}

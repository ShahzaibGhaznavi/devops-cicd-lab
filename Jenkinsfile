
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

        stage('Unit Tests & Coverage') {
            steps {
                sh '''
                    set -e

                    python3 -m venv .venv
                    .venv/bin/python -m pip install \
                      --disable-pip-version-check pytest pytest-cov

                    .venv/bin/python -m pytest \
                      --cov=app \
                      --cov-report=xml:coverage.xml \
                      --cov-report=term \
                      -v

                    test -s coverage.xml
                    echo "Coverage report generated successfully."
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'coverage.xml',
                                     allowEmptyArchive: true
                }
            }
        }

        stage('Trivy Filesystem Scan') {
            steps {
                sh '''
                    set -e
                    trivy --config /dev/null fs \
                      --scanners vuln,misconfig,secret \
                      --format table \
                      --output trivy-report.txt \
                      .

                    cat trivy-report.txt
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
                    docker build --pull \
                      -t devops-cicd-lab:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh '''
                    set -e
                    trivy --config /dev/null image \
                      --ignorefile /dev/null \
                      --skip-files "**/pip/_vendor/bom.cdx.json" \
                      --pkg-types os,library \
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
                              -Dsonar.sources=app.py \
                              -Dsonar.tests=test_app.py \
                              -Dsonar.python.coverage.reportPaths=coverage.xml \
                              -Dsonar.python.version=3.12 \
                              -Dsonar.scm.disabled=true \
                              -Dsonar.exclusions=.venv/**,**/__pycache__/**,.scannerwork/** \
                              -Dsonar.coverage.exclusions=test_app.py
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-cred',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_PASSWORD'
                    )
                ]) {
                    sh '''
                        set -e

                        echo "$DOCKERHUB_PASSWORD" | docker login \
                          -u "$DOCKERHUB_USERNAME" --password-stdin

                        docker tag devops-cicd-lab:${BUILD_NUMBER} \
                          "$DOCKERHUB_USERNAME/devops-cicd-lab:${BUILD_NUMBER}"

                        docker push \
                          "$DOCKERHUB_USERNAME/devops-cicd-lab:${BUILD_NUMBER}"

                        docker tag devops-cicd-lab:${BUILD_NUMBER} \
                          "$DOCKERHUB_USERNAME/devops-cicd-lab:latest"

                        docker push "$DOCKERHUB_USERNAME/devops-cicd-lab:latest"

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
    steps {
        withCredentials([
            file(credentialsId: 'kubeconfig-webapps', variable: 'KUBECONFIG')
        ]) {
            sh '''
                set -e

                kubectl get nodes

                kubectl -n webapps create deployment devops-cicd-lab \
                    --image=shahzaibazeem/devops-cicd-lab:${BUILD_NUMBER} \
                    --dry-run=client -o yaml | kubectl apply -f -

                kubectl -n webapps rollout status deployment/devops-cicd-lab \
                    --timeout=180s

                kubectl -n webapps get deployments,pods,services
            '''
        }
    }
}
        
        stage('Promote Image to Latest') {
            steps {
                sh '''
                    set -e
                    docker tag devops-cicd-lab:${BUILD_NUMBER} \
                      devops-cicd-lab:latest

                    docker image inspect devops-cicd-lab:latest \
                      --format 'Image ID: {{.Id}}'
                '''
            }
        }
    }

    post {
        success {
            emailext(
                to: 'shahzaibazeem558@gmail.com',
                subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """Build successful!

Job: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Status: ${currentBuild.currentResult}
Build URL: ${env.BUILD_URL}
"""
            )
        }

        failure {
            emailext(
                to: 'shahzaibazeem558@gmail.com',
                subject: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """Build failed.

Job: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Status: ${currentBuild.currentResult}
Build URL: ${env.BUILD_URL}

Please check the Jenkins console output.
"""
            )
        }
    }
}


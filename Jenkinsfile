```groovy
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
                    ls -lh coverage.xml
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
                        echo "Trivy filesystem scanner failed."
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

        stage('Promote Image to Latest') {
            steps {
                sh '''
                    set -e
                    docker tag devops-cicd-lab:${BUILD_NUMBER} \
                      devops-cicd-lab:latest

                    echo "Verified build promoted to latest."
                    docker image inspect \
                      devops-cicd-lab:latest \
                      --format 'Image ID: {{.Id}}'
                '''
            }
        }
    }
}
```

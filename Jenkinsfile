pipeline {
    agent { label 'Jenkins-worker01' }
    environment {
        APP_DIR = '/home/ubuntu/workspace/myapp'
        SERVICE_FILE = '/etc/systemd/system/myapp.service'
        VENV_PATH = "venv" 
    }

    stages {
        stage('Setup Environment') {
            steps {
                script {
                    try {
                        sh """
                            echo 'Setting up environment'
                            sudo apt-get update
                            sudo apt install python3-pip -y
                            sudo apt install python3-virtualenv -y
                            cd ${APP_DIR}
                            python3 -m venv $VENV_PATH
                            sudo chown -R ubuntu:ubuntu ${APP_DIR}/venv
                            ./$VENV_PATH/bin/pip install Flask gunicorn pytest requests
                        """
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Environment setup failed.")
                    }
                }
            }
        }

        stage('Deploy Systemd Service') {
            steps {
                script {
                    try {
                        sh """
                            echo 'Deploying systemd service'
                            sudo cp ${APP_DIR}/myapp.service ${SERVICE_FILE}
                            sudo systemctl daemon-reload
                            sudo systemctl enable myapp
                        """
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Deploying systemd service failed.")
                    }
                }
            }
        }

        stage('Start Gunicorn Service') {
            steps {
                script {
                    try {
                        sh """
                            echo 'Starting Gunicorn service'
                            sudo systemctl start myapp && sudo systemctl status myapp || true
                        """
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Starting Gunicorn service failed.")
                    }
                }
            }
        }

        stage('Testing') {
            steps {
                script {
                    try {
                        sh """
                            echo 'Running tests'
                            ./$VENV_PATH/bin/pytest tests.py
                        """
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Tests failed.")
                    }
                }
            }
        }
    }

    triggers {
        pollSCM('H/5 * * * *')  // Polls every 5 minutes for changes; configure according to requirements
    }

    post {
        always {
            script {
                if (currentBuild.result == 'SUCCESS') {
                    slackSend(channel: '#jenkins-job-notifications', message: "Build SUCCESS for myapp - Build #${env.BUILD_NUMBER}")
                } else {
                    slackSend(channel: '#jenkins-job-notifications', message: "Build FAILED for myapp - Build #${env.BUILD_NUMBER}")
                }
            }
        }
    }
}

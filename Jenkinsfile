pipeline {
    agent { label 'Jenkins-worker01' }  // Ensure this node exists

    environment {
        APP_DIR = '/home/ubuntu/workspace/myapp'  // Path to the application directory
        SERVICE_FILE = '/etc/systemd/system/myapp.service'
		VENV_PATH = "venv" 
    }

    stages {

        stage('Setup Environment') {
            steps {
                // 
                sh """
                    echo 'Setup the Python environment and install packages'
                    sudo apt-get update
                    sudo apt install python3-pip -y
                    sudo apt install python3-virtualenv -y
                    cd ${APP_DIR}
                    python3 -m venv $VENV_PATH
                    sudo chown -R ubuntu:ubuntu ${APP_DIR}/venv
                    ./$VENV_PATH/bin/pip install  Flask gunicorn pytest requests
                """
            }
        }

        stage('Deploy Systemd Service') {
            steps {
                sh """
                    echo 'Copy the myapp.service file from the repo to the systemd directory'
                    sudo cp ${APP_DIR}/myapp.service ${SERVICE_FILE}
                    sudo systemctl daemon-reload
                    sudo systemctl enable myapp
                """
            }
        }

        stage('Start Gunicorn Service') {
            steps {
                sh """
                    echo "Start the Gunicorn service for the Flask app"
                    sudo systemctl start myapp && sudo systemctl status myapp
                """
            }
        }
		
		stage('Testing') {
            steps {
                sh """
                    echo "Doing Website testing"
                    ./$VENV_PATH/bin/pytest tests.py
                """
            }
        }
    }

	triggers {
        pollSCM('H/5 * * * *')  // Polls every 5 minutes for changes; configure according to requirements
    }
	
    post {
        success {
            echo 'Flask application deployed successfully!'
            slackSend(channel: '#jenkins-job-notifications', message: "Build FAILED for myapp - Build #${env.BUILD_NUMBER}")

        }
        failure {
            echo 'Deployment failed.'
            slackSend(channel: '#jenkins-job-notifications', message: "Build FAILED for myapp - Build #${env.BUILD_NUMBER}")

        }
    }
}

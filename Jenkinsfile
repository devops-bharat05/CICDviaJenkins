pipeline {
    agent { label 'Jenkins-worker01' }  // Ensure this node exists

    environment {
        APP_DIR = '/home/ubuntu/myapp'  // Path to the application directory
        SERVICE_FILE = '/etc/systemd/system/myapp.service'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the repository containing your Flask app and service file
                git 'https://github.com/devops-bharat05/myapp.git'
            }
        }

        stage('Setup Environment') {
            steps {
                // Setup the Python environment and install packages
                sh """
                    sudo apt-get update
                    sudo apt install python3-pip -y
                    sudo apt install python3-virtualenv -y
                    mkdir -p ${APP_DIR}  // Ensure the application directory exists
                    cd ${APP_DIR}
                    sudo virtualenv venv
                    sudo chown -R ubuntu:ubuntu ${APP_DIR}/venv
                    source venv/bin/activate && pip install Flask gunicorn
                """
            }
        }

        stage('Deploy Systemd Service') {
            steps {
                // Copy the myapp.service file from the repo to the systemd directory
                sh """
                    sudo cp ${APP_DIR}/myapp.service ${SERVICE_FILE}
                    sudo systemctl daemon-reload
                    sudo systemctl enable myapp
                """
            }
        }

        stage('Start Gunicorn Service') {
            steps {
                // Start the Gunicorn service for the Flask app
                sh """
                    sudo systemctl start myapp && sudo systemctl status myapp
                """
            }
        }
    }

    post {
        success {
            echo 'Flask application deployed successfully!'
        }
        failure {
            echo 'Deployment failed.'
        }
    }
}

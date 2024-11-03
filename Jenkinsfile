pipeline {
    agent { label 'Jenkins-worker01' }

    environment {
        APP_DIR = '/home/ubuntu/myapp'  // Path to the application directory
        SERVICE_FILE = '/etc/systemd/system/myapp.service'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the repository containing your Flask app
                git 'https://github.com/devops-bharat05/myapp.git'
            }
        }

        stage('Setup Environment') {
            steps { {
                    sh """
                        sudo apt-get update
                        sudo apt install python3-pip -y
                        sudo apt install python3-virtualenv -y
                        cd ${APP_DIR}
                        sudo virtualenv venv
                        sudo chown -R ubuntu:ubuntu ${APP_DIR}/venv
                        source venv/bin/activate
                        pip install Flask
						pip install gunicorn
                    """
                }
            }
        }

        stage('Create Gunicorn Service') {
            steps {
					{
                    sh """
                        sudo systemctl daemon-reload
                        sudo systemctl enable myapp
                    
                    """
                }
            }
        }

        stage('Start Gunicorn Service') {
            steps {
				{
                    sh """
                    sudo systemctl start myapp && sudo systemctl status myapp
                    """
                }
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

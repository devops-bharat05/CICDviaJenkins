# Jenkins CI/CD Pipeline for Flask Application 🚀

This repository demonstrates a CI/CD pipeline using Jenkins to deploy a Flask application. The setup automates environment setup, deployment, and testing of the Flask application on a Linux server using `systemd` and `gunicorn`. 

![Pipeline Overview](https://via.placeholder.com/800x200.png?text=Jenkins+Pipeline+Overview)  <!-- Replace with actual image link -->

## Project Structure 📁

| File              | Description                                                       |
|-------------------|-------------------------------------------------------------------|
| **Jenkinsfile**   | Pipeline script defining CI/CD stages.                            |
| **app.py**        | Flask application with endpoints to display application information. |
| **myapp.service** | Systemd service file for running the Flask app with gunicorn.     |
| **tests.py**      | Test script for verifying Flask endpoints.                        |

## Pipeline Overview 🛠️

The Jenkins pipeline automates the following steps:
1. **Environment Setup**: Installs Python, pip, and virtual environment. Sets up a virtual environment and installs required packages.
2. **Deploy Systemd Service**: Copies the `myapp.service` file to the systemd directory and enables the service.
3. **Start Gunicorn Service**: Starts the service for the Flask application via systemd.
4. **Testing**: Executes tests on the Flask application using pytest.

![Alt text](images/build_pass.png) <!-- Replace with actual image link -->

### Requirements ✅

- **Jenkins Worker Node** - Ensure you have a Jenkins node labeled `Jenkins-worker01` with SSH access and `sudo` privileges.
- **Python** - Ensure Python 3.x is installed on the server.
- **Network Access** - The application should be accessible on port `5000`.

## Pipeline Stages in `Jenkinsfile` 📜

```groovy
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

    post {
        success {
            echo 'Flask application deployed successfully!'
        }
        failure {
            echo 'Deployment failed.'
        }
    }
}
```

### Application Code (app.py) 🐍

This Flask application provides two endpoints:
- **/name** - Returns the name of the developer.
- **/version** - Returns the current version of the application.

```python
from flask import Flask
app = Flask(__name__)

@app.route('/name')
def get_name():
    return 'Devops Bharat'

@app.route('/version')
def get_version():
    return 'v1.0.0.0'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Systemd Service File (myapp.service) 📝

This systemd service file configures the application to run with gunicorn.

```ini
[Unit]
Description=Gunicorn instance to serve Flask application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/workspace/myapp
Environment="PATH=/home/ubuntu/workspace/myapp/venv/bin"
ExecStart=/home/ubuntu/workspace/myapp/venv/bin/gunicorn -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

### Testing (tests.py) ✅

Tests for the application endpoints are defined in `tests.py`. These tests use `pytest` and `requests` to validate endpoint responses.

```python
import requests
import pytest

BASE_URL = "http://localhost:5000"

def test_get_name():
    response = requests.get(BASE_URL + "/name")
    assert response.status_code == 200
    assert response.text == 'Devops Bharat'

def test_get_version():
    response = requests.get(BASE_URL + "/version")
    assert response.status_code == 200
    assert response.text == 'v1.0.0.0'
```

## Running the Pipeline ▶️

1. **Set Up Jenkins Job**: Create a Jenkins job and link it to this repository.
2. **Run the Job**: Run the pipeline job to deploy the Flask application. Jenkins will automatically go through each stage and handle any errors according to the `post` conditions.

## Monitoring 🖥️

After deployment, monitor the application service with:
```bash
sudo systemctl status myapp
```

Access the application at `http://<your_server_ip>:5000`.

![System Monitoring](https://via.placeholder.com/800x150.png?text=System+Monitoring+View)  <!-- Replace with actual image link -->

## Troubleshooting 🔧

- **Service Issues**: Check systemd logs for error messages:
    ```bash
    sudo journalctl -u myapp
    ```

- **Network Issues**: Verify the application is accessible on the specified port (5000 by default).


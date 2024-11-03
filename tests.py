import requests
import pytest

# Define the base URL of your application
BASE_URL = "http://localhost:5000"  # Change this if your app runs on a different host/port

def test_get_name():
    """Test the /name endpoint."""
    response = requests.get(BASE_URL + "/name")
    assert response.status_code == 200  # Check if the status code is 200 (OK)
    assert response.text == 'Devops Bharat'  # Check the response content

def test_get_version():
    """Test the /version endpoint."""
    response = requests.get(BASE_URL + "/version")
    assert response.status_code == 200  # Check if the status code is 200 (OK)
    assert response.text == 'v1.0.0.0'  # Check the response content

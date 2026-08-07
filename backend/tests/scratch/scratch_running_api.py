import requests

try:
    response = requests.post("http://localhost:8000/api/v1/investigations/", json={"target": "youtube.com", "type": "WEBSITE"})
    print("Status:", response.status_code)
    print("Response:", response.text)
except Exception as e:
    print("Error:", e)

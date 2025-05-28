"""
test_client.py
--------------
A simple test script that sends planner data to the File Exporter Microservice
and downloads the returned file in either CSV or JSON format.

Make sure the microservice (downloader.py) is running locally before executing this.
"""

import requests

# Define the planner data payload to send to the microservice
payload = {
    "data": [
        {"task": "Write microservice", "due_date": "2025-05-21", "duration": "2h"},
        {"task": "Test export", "due_date": "2025-05-22", "duration": "1h"}
    ],
    "format": "csv",  # Change to "json" if you want a .json output file instead
    "fields": ["task", "due_date"]  # Optional: specify fields to include in the export
}

# Send a POST request to the microservice running at localhost on port 5000
response = requests.post("http://127.0.0.1:5000/export", json=payload)

# Save the response content as a downloadable file
# The file format is determined by the 'format' specified in the payload
with open("planner_export.csv", "wb") as f:
    f.write(response.content)

print("File downloaded as 'planner_export.csv'")

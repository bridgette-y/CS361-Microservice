import requests

# Prepare test data
payload = {
    "data": [
        {"task": "Write microservice", "due_date": "2025-05-21", "duration": "2h"},
        {"task": "Test export", "due_date": "2025-05-22", "duration": "1h"}
    ],
    "format": "csv",  # or "json"
    "fields": ["task", "due_date"]
}

# Send the POST request to the local server
response = requests.post("http://127.0.0.1:5000/export", json=payload)

# Save the returned file
with open("planner_export.csv", "wb") as f:
    f.write(response.content)

print("File downloaded as 'planner_export.csv'")

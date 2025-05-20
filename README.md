# CS361-Microservice
# File Exporter Microservice

## Purpose
This microservice receives planner data and returns a downloadable file in either CSV or JSON format.

## Communication Contract

###  Requesting Data
Send a `POST` request to: http://127.0.0.1:5000/export

#### Parameters:
- `data`: List of planner entries (each as a dictionary)
- `format`: `"csv"` or `"json"`
- `fields` *(optional)*: List of strings specifying which fields to include

#### Example Request:
```python
import requests

payload = {
  "data": [{"task": "Study", "due_date": "2025-05-21"}],
  "format": "csv",
  "fields": ["task"]
}
r = requests.post("http://127.0.0.1:5000/export", json=payload)
with open("planner.csv", "wb") as f:
    f.write(r.content)
```
### Receiving Data
The response is a downloadable file (planner.csv or planner.json) served with appropriate headers.

### UML Sequence Diagram
![image](https://github.com/user-attachments/assets/384a5676-d01b-443f-bea4-0997446a0a41)

### Set Up
```python
pip install flask
python downloader.py
```

### Repository

GitHub link: [github.com/bridgette-y/CS361-Microservice]

## Mitigation Plan

**For which teammate did you implement “Microservice A”?**  
Leonardo Reyes Munoz

**What is the current status of the microservice?**  
It is complete and tested with a Python script.

**How will your teammate access your microservice?**  
They should:
- Clone the GitHub repo: [github.com/bridgette-y/CS361-Microservice]
- Run `downloader.py` locally using Python
- Use `requests.post()` from their own code to make requests

**What if they cannot access it?**  
- Contact me via our group Discord or DM
- My schedule is flexible, feel free to message me at any time.
- Let me know **by 5/25 ** so I can implement changes and we have time to test before the next iteration of the project is due

**Other notes**  
- The microservice must be run locally
- Output filenames are fixed
- Do not need to use my test script—just replicate the structure of the request


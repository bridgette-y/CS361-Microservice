"""
downloader.py
--------------
Flask-based microservice to export planner data as CSV or JSON.
Receives structured JSON input via POST, and returns a downloadable file.
"""

from flask import Flask, request, Response, jsonify
import csv
import io
import json

# Initialize Flask app
app = Flask(__name__)

@app.route('/export', methods=['POST'])
def export():
    """
    Endpoint to export planner data as either CSV or JSON.

    Expects a POST request with JSON payload:
    {
        "data": [list of planner entries as dictionaries],
        "format": "csv" or "json",
        "fields": [optional list of field names to include]
    }

    Returns:
        - CSV or JSON file as attachment
        - 400 Bad Request for invalid input
        - 500 Internal Server Error for unhandled exceptions
    """
    try:
        # Parse JSON from the request
        req = request.get_json(force=True)
        data = req.get('data')
        export_format = req.get('format')
        fields = req.get('fields')

        # Basic validation: ensure required keys exist
        if not data or not export_format:
            return jsonify({"error": "Both 'data' and 'format' are required"}), 400

        if export_format not in ['csv', 'json']:
            return jsonify({"error": "Format must be 'csv' or 'json'"}), 400

        # Validate that data is a list of dictionaries
        if not isinstance(data, list) or not all(isinstance(d, dict) for d in data):
            return jsonify({"error": "'data' must be a list of dictionaries"}), 400

        # Optional: Filter fields if provided
        if fields:
            if not all(isinstance(f, str) for f in fields):
                return jsonify({"error": "'fields' must be a list of strings"}), 400
            # Include only specified fields, fill missing fields with empty string
            data = [{k: entry.get(k, "") for k in fields} for entry in data]

        # === JSON Export ===
        if export_format == "json":
            json_output = json.dumps(data, indent=2)
            response = Response(json_output, mimetype='application/json')
            response.headers['Content-Disposition'] = 'attachment; filename=planner.json'
            return response

        # === CSV Export ===
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fields or data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        csv_output = output.getvalue()
        response = Response(csv_output, mimetype='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=planner.csv'
        return response

    except Exception as e:
        # Handle unexpected errors and return 500
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Entry point: run app locally on default port (5000)
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, Response, jsonify
import csv
import io
import json

app = Flask(__name__)

@app.route('/export', methods=['POST'])
def export():
    try:
        req = request.get_json(force=True)

        data = req.get('data')
        export_format = req.get('format')
        fields = req.get('fields')

        if not data or not export_format:
            return jsonify({"error": "Both 'data' and 'format' are required"}), 400

        if export_format not in ['csv', 'json']:
            return jsonify({"error": "Format must be 'csv' or 'json'"}), 400

        # Validate data
        if not isinstance(data, list) or not all(isinstance(d, dict) for d in data):
            return jsonify({"error": "'data' must be a list of dictionaries"}), 400

        # Optional field filtering
        if fields:
            if not all(isinstance(f, str) for f in fields):
                return jsonify({"error": "'fields' must be a list of strings"}), 400
            data = [{k: entry.get(k, "") for k in fields} for entry in data]

        # Handle JSON output
        if export_format == "json":
            response = Response(json.dumps(data, indent=2), mimetype='application/json')
            response.headers['Content-Disposition'] = 'attachment; filename=planner.json'
            return response

        # Handle CSV output
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fields or data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        response = Response(output.getvalue(), mimetype='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=planner.csv'
        return response

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

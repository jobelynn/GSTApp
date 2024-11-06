# app.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GUID = "da03d058-fd4f-4ea3-9889-54701cf2a4a6"

def get_abn_details(abn):
    url = f"https://abr.business.gov.au/json/AbnDetails.aspx?abn={abn}&guid={GUID}"
    response = requests.get(url)
    return response.json()

@app.route('/verify', methods=['POST'])
def verify_abns():
    data = request.get_json()
    abns = data.get("abns", [])
    results = []

    for abn in abns:
        abn_data = get_abn_details(abn)
        gst_compliant = abn_data.get("GST", False)
        results.append({
            "abn": abn,
            "gst_compliant": gst_compliant,
            "entity_name": abn_data.get("EntityName", "N/A")
        })

    return jsonify(results), 200

if __name__ == "__main__":
    app.run(debug=True)

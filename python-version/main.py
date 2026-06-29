import json, unittest, datetime
from flask import Flask

app = Flask(__name__)

# Load the three json files
with open("./data-1.json", "r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json", "r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json", "r") as f:
    jsonExpectedResult = json.load(f)


# Convert json data from format 1 to the expected format
def convertFromFormat1(jsonObject):
    locationParts = jsonObject["location"].split("/")
    result = {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": {
            "country": locationParts[0],
            "city": locationParts[1],
            "area": locationParts[2],
            "factory": locationParts[3],
            "section": locationParts[4]
        },
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    }
    return result


# Convert json data from format 2 to the expected format
def convertFromFormat2(jsonObject):
    dt = datetime.datetime.strptime(
        jsonObject["timestamp"],
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    timestamp = round(
        (dt - datetime.datetime(1970, 1, 1)).total_seconds() * 1000
    )
    result = {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp,
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },
        "data": jsonObject["data"]
    }
    return result


def main(jsonObject):
    if jsonObject.get('device') is None:
        return convertFromFormat1(jsonObject)
    else:
        return convertFromFormat2(jsonObject)


# Run tests and collect results
def run_tests():
    results = []

    tests = [
        {
            "name": "Sanity Test",
            "desc": "Ensures the expected result JSON is valid",
            "fn": lambda: json.loads(json.dumps(jsonExpectedResult)) == jsonExpectedResult
        },
        {
            "name": "Data Type 1 Conversion",
            "desc": "Converts flat location string format to nested format",
            "fn": lambda: main(jsonData1) == jsonExpectedResult
        },
        {
            "name": "Data Type 2 Conversion",
            "desc": "Converts device-object + ISO timestamp format to nested format",
            "fn": lambda: main(jsonData2) == jsonExpectedResult
        },
    ]

    all_passed = True
    for t in tests:
        try:
            passed = t["fn"]()
            results.append({"name": t["name"], "desc": t["desc"], "passed": passed, "error": None})
            if not passed:
                all_passed = False
        except Exception as e:
            results.append({"name": t["name"], "desc": t["desc"], "passed": False, "error": str(e)})
            all_passed = False

    return results, all_passed


@app.route("/")
def index():
    results, all_passed = run_tests()

    rows = ""
    for r in results:
        status_badge = (
            '<span style="background:#22c55e;color:#fff;padding:3px 12px;border-radius:999px;font-size:13px;font-weight:600;">PASS</span>'
            if r["passed"] else
            '<span style="background:#ef4444;color:#fff;padding:3px 12px;border-radius:999px;font-size:13px;font-weight:600;">FAIL</span>'
        )
        error_row = f'<p style="color:#ef4444;font-size:13px;margin:4px 0 0 0;">Error: {r["error"]}</p>' if r["error"] else ""
        rows += f"""
        <div style="background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:16px 20px;margin-bottom:12px;display:flex;align-items:flex-start;justify-content:space-between;gap:16px;">
            <div>
                <p style="font-weight:600;margin:0 0 4px 0;font-size:15px;">{r['name']}</p>
                <p style="color:#6b7280;margin:0;font-size:13px;">{r['desc']}</p>
                {error_row}
            </div>
            <div style="flex-shrink:0;">{status_badge}</div>
        </div>
        """

    summary_color = "#22c55e" if all_passed else "#ef4444"
    summary_text = f"All {len(results)} tests passed" if all_passed else f"Some tests failed"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Data Format Converter — Test Results</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f3f4f6; min-height: 100vh; padding: 40px 16px; }}
        .card {{ max-width: 640px; margin: 0 auto; background: #fff; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.08); padding: 36px; }}
        h1 {{ font-size: 22px; font-weight: 700; margin-bottom: 4px; }}
        .sub {{ color: #6b7280; font-size: 14px; margin-bottom: 28px; }}
        .summary {{ border-radius: 10px; padding: 14px 18px; margin-bottom: 24px; font-weight: 600; font-size: 15px; color: #fff; background: {summary_color}; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>Data Format Converter</h1>
        <p class="sub">Virtual Internship Task &mdash; JSON Format Normalization</p>
        <div class="summary">{summary_text}</div>
        {rows}
        <p style="color:#9ca3af;font-size:12px;margin-top:20px;text-align:center;">Converts IoT device data from two input formats into a unified output format.</p>
    </div>
</body>
</html>"""
    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

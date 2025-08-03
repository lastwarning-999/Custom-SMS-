from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)
KEY_FILE = "key.txt"

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            return f.read().strip()
    return "raj"  # default key

def save_key(new_key):
    with open(KEY_FILE, "w") as f:
        f.write(new_key.strip())

def send_sms(text, mobile):
    url = "https://appbowl.com/api/sms/send-sms"

    headers = {
        "Host": "appbowl.com",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "sec-ch-ua-platform": "\"Android\"",
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"
        ),
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
        "sec-ch-ua-mobile": "?1",
        "Accept": "*/*",
        "Origin": "https://appbowl.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://appbowl.com/",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9"
    }

    data = {
        "name": text,
        "mobile": mobile
    }

    return requests.post(url, headers=headers, data=json.dumps(data))

@app.route("/", methods=["GET"])
def api():
    # Key change functionality
    new_key = request.args.get("key_change")
    if new_key:
        save_key(new_key)
        return jsonify({
            "status": "success",
            "message": f"API key updated to: {new_key}",
            "credit": "API OWNER BY: @hardhackar007"
        })

    # Normal SMS sending
    text = request.args.get("text")
    mobile = request.args.get("mobile")
    count = request.args.get("count", default="1")
    user_key = request.args.get("key")

    if not user_key or user_key != load_key():
        return jsonify({
            "status": "unauthorized",
            "message": "Invalid or missing key.",
            "credit": "API OWNER BY: @hardhackar007"
        }), 403

    if not text or not mobile:
        return jsonify({
            "status": "error",
            "message": "Missing 'text' or 'mobile'.",
            "credit": "API OWNER BY: @hardhackar007"
        }), 400

    try:
        count = int(count)
        success_count = 0
        responses = []

        for i in range(count):
            res = send_sms(text, mobile)
            try:
                res_data = res.json()
            except Exception:
                res_data = res.text
            responses.append({
                "try": i + 1,
                "status_code": res.status_code,
                "response": res_data
            })
            if res.status_code == 200:
                success_count += 1

        return jsonify({
            "status": "success",
            "total_sent": success_count,
            "requested": count,
            "mobile": mobile,
            "credit": "API OWNER BY: @hardhackar007",
            "responses": responses
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "credit": "API OWNER BY: @hardhackar007"
        }), 500

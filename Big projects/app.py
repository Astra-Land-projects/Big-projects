from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# پروکسی Tor (باید Tor Browser یا Tor Service اجرا باشد)
TOR_PROXY = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050",
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        
        print(f"📩 پیام: {user_message}")
        
        response = requests.get(
            f"https://text.pollinations.ai/{requests.utils.quote(user_message)}",
            params={"model": "openai", "seed": "42"},
            proxies=TOR_PROXY,
            timeout=60
        )
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            return jsonify({"reply": response.text.strip()})
        else:
            return jsonify({"reply": f"❌ خطا: {response.status_code}"}), 200
            
    except Exception as e:
        print(f"❌ خطا: {e}")
        return jsonify({"reply": f"❌ خطا: {str(e)}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify
import hmac, hashlib, time
import requests
import json

app = Flask(__name__)

# Your Bybit Testnet API keys
API_KEY = "XZVy09QUa40VQOVq4v"
API_SECRET = "Qc6PtmFzLYYuXaBD7pFV5T1haVoVeCyYwnqP"

def send_order(side, symbol="XAUUSDT", qty=1, tp=0, sl=0):
    timestamp = int(time.time() * 1000)
    endpoint = "https://api-testnet.bybit.com/v2/private/order/create"

    params = {
        "api_key": API_KEY,
        "symbol": symbol,
        "side": side,
        "order_type": "Market",
        "qty": qty,
        "time_in_force": "GoodTillCancel",
        "timestamp": timestamp
    }

    if tp > 0: params["take_profit"] = str(tp)
    if sl > 0: params["stop_loss"] = str(sl)

    param_str = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
    sign = hmac.new(bytes(API_SECRET, "utf-8"), param_str.encode("utf-8"), hashlib.sha256).hexdigest()
    params["sign"] = sign

    res = requests.post(endpoint, data=params)
    return res.json()

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    print("Alert Received:", data)

    if "BUY" in data["message"]:
        send_order("Buy")
    elif "SELL" in data["message"]:
        send_order("Sell")

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)

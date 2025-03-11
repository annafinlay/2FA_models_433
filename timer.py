import time
from flask import session, request
from physical_token_2fa import app2, USER_PHYSICAL_KEY  # Import the existing app
from sms_2fa import app2, USER_CREDENTIALS
from totp_2fa import app3, USER_SECRET

@app2.before_request
def start_timer():
    if request.endpoint in ["login", "use_physical_key"] and request.method == "POST":
        session["auth_start_time"] = time.time()

@app2.after_request
def stop_timer(response):
    if request.endpoint == "use_physical_key" and request.method == "POST":
        if "auth_start_time" in session:
            total_time = time.time() - session.pop("auth_start_time", None)
            response.set_data(response.get_data(as_text=True) + f"<p>Authentication time: {total_time:.4f} seconds</p>")
    return response

if __name__ == "__main__":
    #Change app2 to app2 or app3
    app2.run(debug=True, port=5001)

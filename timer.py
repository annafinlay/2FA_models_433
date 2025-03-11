import time
from flask import session, request
from physical_token_2fa import app1, USER_PHYSICAL_KEY  # Import the existing app
from sms_2fa import app2, USER_CREDENTIALS
from totp_2fa import app3, USER_SECRET

@app2.before_request
def start_timer():
    if request.endpoint in ["login", "use_physical_key"] and request.method == "POST":
        session["auth_start_time"] = time.time()

@app2.after_request
def stop_timer(response):
    if request.endpoint in ["use_physical_key", "login"] and request.method == "POST": #added login to the check
        if "auth_start_time" in session:
            total_time = time.time() - session.pop("auth_start_time", None)
            response_data = response.get_data(as_text=True)
            if isinstance(response_data, str): #check if response_data is a string before appending
                response_data += f"<p>Authentication time: {total_time:.4f} seconds</p>"
                response.set_data(response_data.encode('utf-8')) #encode back to bytes
            else:
                print(f"Warning: response_data is not a string. Authentication time: {total_time:.4f} seconds.") #print time to console if response is not a string.
    return response

if __name__ == "__main__":
    #Change app2 to app2 or app3
    app2.run(debug=True, port=5002)

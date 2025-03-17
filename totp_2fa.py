import os
import io
import pyotp
import qrcode
import time
from flask import Flask, request, session, redirect, url_for, send_file, make_response

app3 = Flask(__name__)
app3.secret_key = os.urandom(24)  # Secure session key

# Generate a new secret key for the TOTP
USER_SECRET = pyotp.random_base32()

@app3.route("/", methods=["GET", "POST"])
def login():
    increment_api_call_count()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "user" and password == "password123":
            session["username"] = username
            session["auth_start_time"] = time.time()  # Start timing authentication
            return redirect(url_for("show_qr"))
        else:
            return "Invalid credentials"
    
    return '''
    <h2>Login</h2>
    <form method="post">
        Username: <input type="text" name="username" required><br>
        Password: <input type="password" name="password" required><br>
        <input type="submit" value="Login">
    </form>
    '''

@app3.route("/setup")
def show_qr():
    increment_api_call_count()
    if "username" not in session:
        return redirect(url_for("login"))
    
    return '''
    <h2>Scan this QR Code with Google Authenticator:</h2>
    <img src="/qr" alt="QR Code" />
    <br><br>
    <a href="/verify">Continue to Verification</a>
    '''

@app3.route("/qr")
def qr_code():
    increment_api_call_count()
    if "username" not in session:
        return redirect(url_for("login"))

    totp = pyotp.TOTP(USER_SECRET)
    qr_url = totp.provisioning_uri(name="user@example.com", issuer_name="Mock 2FA App")
    
    # Generate QR code
    img = qrcode.make(qr_url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    # Prevent caching issues in Chrome
    response = make_response(send_file(buf, mimetype="image/png"))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    return response

@app3.route("/verify", methods=["GET", "POST"])
def verify_totp():
    increment_api_call_count()
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        entered_code = request.form.get("totp")
        totp = pyotp.TOTP(USER_SECRET)
        if totp.verify(entered_code):
            if "auth_start_time" in session:
                auth_time = time.time() - session.pop("auth_start_time")
                return f"Login Successful! Authentication time: {auth_time:.4f} seconds"
            else:
                return "Login Successful!"
        else:
            return "Invalid OTP. Try again."

    return '''
    <h2>Enter the 6-digit TOTP code from your app:</h2>
    <form method="post">
        OTP: <input type="text" name="totp" required>
        <input type="submit" value="Verify">
    </form>
    '''
    
@app3.route("/api_count")
def api_count():
    return f"Total API Calls: {get_api_call_count()}"

if __name__ == "__main__":
    app3.run(debug=True)

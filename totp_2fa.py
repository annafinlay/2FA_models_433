import os
import io
import pyotp
import qrcode
from flask import Flask, request, session, redirect, url_for, send_file

app3 = Flask(__name__)
app3.secret_key = os.urandom(24)  # Secure session key

# Generate a new secret key for the TOTP 
USER_SECRET = pyotp.random_base32()

@app3.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "user" and password == "password123":
            session["username"] = username
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
    if "username" not in session:
        return redirect(url_for("login"))
    
    totp = pyotp.TOTP(USER_SECRET)
    provisioning_uri = totp.provisioning_uri(name="user@example.com", issuer_name="Mock 2FA App")
    
    # Display the QR code generated locally at the /qr endpoint.
    return f'''
    <h2>Scan this QR Code with Google Authenticator:</h2>
    <img src="/qr" alt="QR Code" />
    <br><br>
    <a href="/verify">Continue to Verification</a>
    <br><br>
    <p>If the QR code does not work, manually enter this secret key in Google Authenticator:</p>
    <strong>{USER_SECRET}</strong>
    '''

@app3.route("/qr")
def qr_code():
    if "username" not in session:
        return redirect(url_for("login"))
    
    totp = pyotp.TOTP(USER_SECRET)
    qr_url = totp.provisioning_uri(name="user@example.com", issuer_name="Mock 2FA App")
    
    # Generate QR code 
    img = qrcode.make(qr_url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

@app3.route("/verify", methods=["GET", "POST"])
def verify_totp():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        entered_code = request.form["totp"]
        totp = pyotp.TOTP(USER_SECRET)
        if totp.verify(entered_code):
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

if __name__ == "__main__":
    app3.run(debug=True)

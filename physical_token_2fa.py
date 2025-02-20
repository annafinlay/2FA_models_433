from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure session key

# Simulated "hardware token"
USER_PHYSICAL_KEY = "secure-physical-token"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "user" and password == "password123":
            session["username"] = username
            return redirect(url_for("use_physical_key"))
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

@app.route("/use_key", methods=["GET", "POST"])
def use_physical_key():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        entered_key = request.form["physical_key"]
        if entered_key == USER_PHYSICAL_KEY:
            return "Login Successful!"
        else:
            return "Invalid Key. Try again."

    return '''
    <h2>Insert Your Security Key</h2>
    <p>Press the button below to simulate inserting a physical security key.</p>
    <form method="post">
        <input type="hidden" name="physical_key" value="secure-physical-token">
        <input type="submit" value="Use Security Key">
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, session, redirect, url_for
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random key

# Simulated user credentials 
USER_CREDENTIALS = {"user": "password123"}

# Generate 6-digit OTP  
def generate_otp():
    return str(random.randint(100000, 999999))

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session["username"] = username
            otp = generate_otp()
            session["otp"] = otp  # Store OTP in session
            
            print(f"Simulated SMS: Your OTP is {otp}")  # Simulating sending OTP
            
            return redirect(url_for("verify_otp"))
        else:
            return "Invalid username or password. Try again."

    return render_template("login.html")

@app.route("/verify", methods=["GET", "POST"])
def verify_otp():
    if "username" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        entered_otp = request.form["otp"]
        if entered_otp == session.get("otp"):
            return "Login Successful!"
        else:
            return "Invalid OTP. Try again."

    return render_template("verify.html")

if __name__ == "__main__":
    app.run(debug=True)

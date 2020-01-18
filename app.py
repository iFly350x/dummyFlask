from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "sup"
app.permanent_session_lifetime = timedelta(seconds=1)
app.debug = True

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user
        pwd = request.form["password"]
        session["pwd"] = pwd
        return redirect(url_for("user"))
    else:
        if "user" in session and "pwd" in session:
            return redirect(url_for("user"))

        return render_template("login.html", title = "login")

@app.route("/user")
def user():
    if "pwd" in session and "user" in session:
        user = session["user"]
        pwd = session["pwd"]
        return f"Your Password: {pwd} and Username:  {user}"
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged Out", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(port=8000)

from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "sup"
app.permanent_session_lifetime = timedelta(days=10)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.debug = True

db = SQLAlchemy(app)

class users(db.Model):
    """docstring for users"""
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))    

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

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
        flash("Login Succuful", "info")
        return redirect(url_for("user"))

        found_user = users.query.filter_by(name=user).first()

        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()
    else:
        if "user" in session and "pwd" in session:
            flash("You're already logged in!")
            return redirect(url_for("user"))
    return render_template("login.html", title = "login")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    password = None

    if "pwd" in session and "user" in session:
        user = session["user"]
        pwd = session["pwd"]
        if request.method =="POST":
            email = request.form["email"]
            password = request.form["password"]
            session["email"] = email
            session["password"] = password
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Login credentials saved ")
        else:
            if "email" in session and "password" in session:
                email = session["email"]
                password = session["password"]

        return render_template("user.html", user=user, title=user, email=email, password=password)

    else:
        flash("Log Back In")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "user" in session and "pwd" in session:
        user = ["user"]
        pwd = ["pwd"]
        flash("Logged Out", "info")
    session.pop("user", None)
    session.pop("email", None)
    session.pop("password", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    db.create_all()
    app.run()

from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = "sup"
app.debug = True

@app.route("/home")
def home():
    return render_template("index.html", title = "Hello")

@app.route("/login")
@app.route("/", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        session["user"] = user
        pwd = request.form["password"]
        session["pwd"] = pwd
        return redirect(url_for("user"))
        # return redirect(url_for("password", passwd = pwd))
    else:
         return render_template("login.html", title = "login")

@app.route("/user")
def user():
    if "pwd" in session and "user" in session:
        user = session["user"]
        pwd = session["pwd"]
        return f"Your Password: {pwd} and Username:  {user}"
    else:
        return redirect(url_for("login"))

# @app.route("<PWD>")
# def password(paswd):
#     return f"<h1>{paswd}</h1>"

if __name__ == "__main__":
    app.run(port=8000)

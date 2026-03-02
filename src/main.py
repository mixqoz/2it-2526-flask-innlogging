# Algoritme som bruker salt & pepper X
# Krypteringsfunksjon X

# TODO: Lagring av brukerdata - Ser på det imorgen

from flask import Flask, render_template, request, redirect, session
from user import User
from pprint import pprint

# Temporary (RAM lagring)
users = {} # Type {[str, User]}

app = Flask(__name__)
# sessions require a secret key; in production use a secure random value
app.secret_key = "dev"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def get_register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def post_register():
    form_data = request.form.to_dict()
    username = form_data.get("username", "").strip()
    password = form_data.get("password", "")

    # empty fields
    if not username or not password:
        return render_template("register.html", error="Både brukernavn og passord må fylles ut", form=form_data)

    # duplicate username
    if username.lower() in users:
        return render_template("register.html", error="Brukernavnet er allerede tatt", form=form_data)

    # create user
    users[username.lower()] = User(username, password)
    pprint(users)
    return redirect("/")


@app.route("/login")
def get_login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def post_login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    # check existence
    if not username or username.lower() not in users:
        return render_template("login.html", error="Wrong password or username", form=request.form)

    user = users.get(username.lower())
    if not user or not user.check_password(password):
        return render_template("login.html", error="Wrong password or username", form=request.form)

    session["user"] = user
    session["logged_in"] = True
    return redirect("/")

# Dev mode:
if __name__ == "__main__":
    app.run(debug=True)

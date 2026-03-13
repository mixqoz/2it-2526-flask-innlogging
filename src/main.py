from flask import Flask, render_template, request, redirect, session
from decorators import login_required
from user import User, get_all
from pprint import pprint

# Temporary (RAM lagring)
users = get_all() # Type {[str, User]}

app = Flask(__name__)
app.secret_key = "3hfdsajfhskruk"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/log-out")
def log_out():
    session.clear()
    return redirect("/")

@app.route("/register")
def get_register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def post_register():
    # copy form data to a dict so we can reuse it if validation fails
    form_data = request.form.to_dict()
    username = form_data.get("username", "").strip()
    password = form_data.get("password", "").strip()
    fornavn = form_data.get("fornavn", "").strip()
    etternavn = form_data.get("etternavn", "").strip()

    # empty fields
    if not username and not password:
        return render_template(
            "register.html",
            error="Brukernavn og passord må fylles ut",
            form=form_data,
        )

    if not username:
        return render_template(
            "register.html",
            error="Brukernavn må fylles ut",
            form=form_data,
        )

    if not password:
        return render_template(
            "register.html",
            error="Passord må fylles ut",
            form=form_data,
        )

    # already exists?
    if username.lower() in users:
        return render_template(
            "register.html",
            error="Brukernavnet er allerede tatt",
            form=form_data,
        )

    # create and persist the user
    user = User(username=username, password=password, fornavn=fornavn, etternavn=etternavn)
    users[user.username.lower()] = user

    # only store the username in session (objects are not JSON serializable)
    session["user"] = user.username
    session["logged_in"] = True
    pprint(users)
    return redirect("/")

@app.route("/min-profil")
@login_required
def min_profil():
    username = session.get("user")
    current_user = users.get(username.lower()) if username else None
    return render_template("min_profil.html", user=current_user)

@app.route("/log-in")
def get_login():
    return render_template("login.html")

@app.route("/log-in", methods=["POST"])
def post_login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if not username and not password:
        return render_template(
            "login.html",
            error_msg="Både brukernavn og passord må fylles ut.",
            form=request.form,
        )

    if not username:
        return render_template(
            "login.html",
            error_msg="Brukernavn må fylles ut.",
            form=request.form,
        )

    if not password:
        return render_template(
            "login.html",
            error_msg="Passord må fylles ut.",
            form=request.form,
        )

    user = users.get(username.lower(), None)
    if not user:
        return render_template(
            "login.html",
            error_msg="Brukeren finnes ikke.",
            form=request.form,
        )

    if not user.check_password(password):
        return render_template(
            "login.html",
            error_msg="Feil passord.",
            form=request.form,
        )

    session["user"] = user.username
    session["logged_in"] = True
    return redirect("/")

# make the users dictionary available in every template
@app.context_processor
def inject_users():
    return dict(users=users)


@app.route("/comment/<post_id>", methods=["POST"])
def comment(post_id):
    if not session.get("logged_in"):
        return "du må logge inn :("

    form_data = request.form
    comment_text = form_data.get("comment", "").strip()
    if not comment_text:
        return "Kommentar kan ikke være tom."

    return "OK"



# Dev mode:
if __name__ == "__main__":
    app.run(debug=True)

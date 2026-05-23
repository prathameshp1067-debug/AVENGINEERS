from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# ---------------- CONFIG ----------------

app.config['SECRET_KEY'] = 'avengineerssecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# If user not logged in
login_manager.login_view = "signin"

# ---------------- DATABASE MODEL ----------------

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(150), unique=True, nullable=False)

    password = db.Column(db.String(150), nullable=False)


# ---------------- USER LOADER ----------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- SIGN UP ----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        # Check existing user
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already exists"

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create user
        new_user = User(
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect("/signin")

    return render_template("signup.html")


# ---------------- SIGN IN ----------------

@app.route("/signin", methods=["GET", "POST"])
def signin():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            return redirect("/")

        return "Invalid Email or Password"

    return render_template("signin.html")


# ---------------- LOGOUT ----------------

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/signin")


# ---------------- HOME ----------------

@app.route("/")
@login_required
def home():
    return render_template("index.html")


# ---------------- TEAM ----------------

@app.route("/team")
@login_required
def team():
    return render_template("team.html")


# ---------------- VISION ----------------

@app.route("/vision")
@login_required
def vision():
    return render_template("vision.html")


# ---------------- ACHIEVEMENTS ----------------

@app.route("/achievements")
@login_required
def achievements():
    return render_template("achievements.html")


# ---------------- TEAMWORK ----------------

@app.route("/teamwork")
@login_required
def teamwork():
    return render_template("teamwork.html")


# ---------------- TEAMWORK DETAIL ----------------

@app.route("/teamwork/<media>")
@login_required
def teamwork_detail(media):
    return render_template("teamwork_detail.html", media=media)


# ---------------- CONTACT ----------------

@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        print(f"Contact form submitted: {name}, {email}, {message}")

        return "Thank you for contacting us!"

    return render_template("contact.html")


# ---------------- NEWS ----------------

@app.route("/news")
@login_required
def news():

    updates = [

        {
            "title": "New Jet Prototype Tested",
            "content": "Our team successfully tested the latest jet prototype with improved aerodynamics."
        },

        {
            "title": "Avengineers Won Innovation Award",
            "content": "We received the National Innovation Award for aerospace engineering excellence."
        }

    ]

    return render_template("news.html", updates=updates)


# ---------------- CREATE DATABASE ----------------

with app.app_context():
    db.create_all()


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
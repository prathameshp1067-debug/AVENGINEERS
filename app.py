from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Store users temporarily
users = {}

# ---------------- SIGNUP PAGE ----------------

@app.route("/", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        # Save user
        users[email] = password

        # Redirect to home page
        return redirect("/home")

    return render_template("signup.html")


# ---------------- SIGNIN PAGE ----------------

@app.route("/signin", methods=["GET", "POST"])
def signin():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        # Check user
        if email in users and users[email] == password:

            return redirect("/home")

        return "Invalid Email or Password"

    return render_template("signin.html")


# ---------------- HOME PAGE ----------------

@app.route("/home")
def home():
    return render_template("index.html")


# ---------------- OTHER PAGES ----------------

@app.route("/team")
def team():
    return render_template("team.html")


@app.route("/vision")
def vision():
    return render_template("vision.html")


@app.route("/achievements")
def achievements():
    return render_template("achievements.html")


@app.route("/teamwork")
def teamwork():
    return render_template("teamwork.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/news")
def news():

    updates = [

        {
            "title": "New Jet Prototype Tested",
            "content": "Our team successfully tested the latest jet prototype."
        },

        {
            "title": "Avengineers Won Innovation Award",
            "content": "We received the National Innovation Award."
        }

    ]

    return render_template("news.html", updates=updates)


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
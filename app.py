from flask import Flask, render_template, request, redirect

app = Flask(__name__)

users = {}

# SIGNUP PAGE
@app.route("/", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        users[email] = password

        return redirect("/signin")

    return render_template("signup.html")


# SIGNIN PAGE
@app.route("/signin", methods=["GET", "POST"])
def signin():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if email in users and users[email] == password:

            return redirect("/home")

        return "Invalid Email or Password"

    return render_template("signin.html")


# HOME PAGE
@app.route("/home")
def home():
    return render_template("index.html")


# TEAM PAGE
@app.route("/team")
def team():
    return render_template("team.html")


# VISION PAGE
@app.route("/vision")
def vision():
    return render_template("vision.html")


# ACHIEVEMENTS PAGE
@app.route("/achievements")
def achievements():
    return render_template("achievements.html")


# GALLERY PAGE
@app.route("/teamwork")
def teamwork():
    return render_template("teamwork.html")


@app.route("/teamwork/<media>")
def teamwork_detail(media):
    return render_template("teamwork_detail.html", media=media)

# CONTACT PAGE
@app.route("/contact")
def contact():
    return render_template("contact.html")


# NEWS PAGE
@app.route("/news")
def news():

    updates = [

        {
            "title": "New Jet Prototype Tested",
            "content": "Prototype tested successfully"
        },

        {
            "title": "Innovation Award",
            "content": "Avengineers won award"
        }

    ]

    return render_template("news.html", updates=updates)


if __name__ == "__main__":
    app.run(debug=True)
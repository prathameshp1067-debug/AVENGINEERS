from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Store users temporarily
users = {}


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
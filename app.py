from flask import Flask, render_template, request

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Team route
@app.route("/team")
def team():
    return render_template("team.html")

# Vision route
@app.route("/vision")
def vision():
    return render_template("vision.html")

# Achievements route
@app.route("/achievements")
def achievements():
    return render_template("achievements.html")

# Teamwork gallery route
@app.route("/teamwork")
def teamwork():
    return render_template("teamwork.html")

# Teamwork detail subpage route
@app.route("/teamwork/<media>")
def teamwork_detail(media):
    return render_template("teamwork_detail.html", media=media)

# Contact route
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        # For now, just print to console (later you can save to DB or send email)
        print(f"Contact form submitted: {name}, {email}, {message}")
        return "Thank you for contacting us!"
    return render_template("contact.html")

@app.route("/news")
def news():
    # Example data: you can later load this from a database or file
    updates = [
        {"title": "New Jet Prototype Tested", "content": "Our team successfully tested the latest jet prototype with improved aerodynamics."},
        {"title": "Avengineers Won Innovation Award", "content": "We received the National Innovation Award for aerospace engineering excellence."},
        {"title": "Collaboration with ISRO", "content": "Avengineers has made a new Prototype."}
    ]
    return render_template("news.html", updates=updates)


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, render_template, request, redirect, jsonify
import math

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
            "date": "2026-08-20",
            "content": "Prototype tested successfully with improved aerodynamics.",
            "image": "work12.jpg"
        },
        {
            "title": "Avengineers Won Innovation Award",
            "date": "2026-08-15",
            "content": "We received the National Innovation Award for aerospace engineering excellence.",
            "image": "award.jpg"
        }
    ]
    return render_template("news.html", updates=updates)


# =========================
# AIRCRAFT DESIGNER PAGE
# =========================

@app.route("/designer")
def designer():
    return render_template("designer.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json() or {}

    # Required inputs
    if "wingSpan" not in data or "wingArea" not in data or "weight" not in data or "payload" not in data:
        return jsonify({"error": "Wing Span, Wing Area, Weight, and Payload are required"}), 400

    b = float(data["wingSpan"])   # Wing span (m)
    S = float(data["wingArea"])   # Wing area (m²)
    W = float(data["weight"])     # Total weight (kg)
    P_load = float(data["payload"]) # Payload (kg)

    # Constants / ratios
    taper_ratio = 0.6
    tc_ratio = 0.12
    vh_ratio = 0.22
    vv_ratio = 0.1
    bh_ratio = 0.35
    hv_ratio = 0.18
    fuselage_factor = 0.75
    thrust_to_weight = 0.8

    # Wing geometry
    AR = round((b**2) / S, 2)
    c_root = round((2 * S) / (b * (1 + taper_ratio)), 3)
    c_tip = round(taper_ratio * c_root, 3)
    MAC = round((2/3) * c_root * (1 + taper_ratio + taper_ratio**2) / (1 + taper_ratio), 3)
    t_max = round(tc_ratio * c_root, 3)

    # Tail
    Sh = round(vh_ratio * S, 3)
    Sv = round(vv_ratio * S, 3)
    bh = round(bh_ratio * b, 3)
    hv = round(hv_ratio * b, 3)

    # Fuselage & CG
    Lf = round(fuselage_factor * b, 3)
    LE = 0.28
    CG_LE = round(0.3 * MAC, 3)
    CG_nose = round(LE + CG_LE, 3)

    # Landing gear
    WB = round(0.22 * Lf, 3)
    MG = round(CG_nose - 0.03, 3)

    # Thrust & Power
    T_req = round(W * thrust_to_weight, 2)
    T_req_N = round(T_req * 9.81, 2)

    # Motor KV, Propeller Diameter & Pitch (simple scaling rules by weight)
    if W < 1.0:
        motorKV = 1200
        prop_diameter = 9
        prop_pitch = 5
    elif W < 2.0:
        motorKV = 1000
        prop_diameter = 11
        prop_pitch = 6
    elif W < 3.0:
        motorKV = 800
        prop_diameter = 13
        prop_pitch = 7
    else:
        motorKV = 600
        prop_diameter = 15
        prop_pitch = 8

    # Performance (simple estimates)
    stall_speed = round(math.sqrt((2 * W * 9.81) / (1.225 * S * 1.5)), 2)
    cruise_speed = round(stall_speed * 1.7, 2)
    max_speed = round(stall_speed * 2.7, 2)
    takeoff_distance = round((stall_speed ** 2) / (2 * 9.81), 2)

    results = {
        "aircraftType": data.get("aircraftType", "Trainer"),
        "wingShape": data.get("wingShape", "Elliptical"),
        "wingSpan": round(b * 39.37, 2),   # inches
        "wingArea": round(S * 1550, 2),    # sq.in
        "aspectRatio": AR,

        # Tail
        "hTailArea": round(Sh * 1550, 2),
        "vTailArea": round(Sv * 1550, 2),
        "hTailSpan": round(bh * 39.37, 2),
        "vTailHeight": round(hv * 39.37, 2),

        # Propulsion
        "motor": f"Brushless {motorKV}KV",
        "motorKV": motorKV,
        "esc": "40A",
        "propeller": f"{prop_diameter}x{prop_pitch}",
        "propDiameter": prop_diameter,
        "propPitch": prop_pitch,
        "requiredThrust": T_req,

        # Performance
        "cruiseSpeed": cruise_speed,
        "maxSpeed": max_speed,
        "flightTime": 20,
        "takeoffDistance": takeoff_distance,
        "stallSpeed": stall_speed,

        # Extra
        "payload": P_load,
        "estimatedWeight": W
    }

    return jsonify(results)




if __name__ == "__main__":
    app.run(debug=True)

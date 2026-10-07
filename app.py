from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sujith@2002",
        database="userprofiledb"
    )

# ---------- START ----------
@app.route("/")
def home():
    return redirect("/register")

# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        mobile = request.form["mobile"]
        address = request.form["address"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO users 
            (first_name, last_name, mobile, address, email, password)
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (fname, lname, mobile, address, email, password)
        )
        db.commit()
        cursor.close()
        db.close()

        return redirect("/login")

    return render_template("register.html")

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user:
            session["user"] = user
            return redirect("/profile")

        return "Invalid credentials"

    return render_template("login.html")

# ---------- PROFILE ----------
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/login")

    return render_template("profile.html", user=session["user"])

# ---------- EDIT PROFILE ----------
@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        mobile = request.form["mobile"]
        address = request.form["address"]

        user_id = session["user"]["id"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            UPDATE users
            SET first_name=%s, last_name=%s, mobile=%s, address=%s
            WHERE id=%s
            """,
            (fname, lname, mobile, address, user_id)
        )
        db.commit()
        cursor.close()
        db.close()

        # update session data
        session["user"]["first_name"] = fname
        session["user"]["last_name"] = lname
        session["user"]["mobile"] = mobile
        session["user"]["address"] = address

        return redirect("/profile")

    return render_template("edit_profile.html", user=session["user"])

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)

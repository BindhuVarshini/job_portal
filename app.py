from flask import Flask, render_template, request, redirect, session
import pymysql
import os

app = Flask(__name__)
app.secret_key = "secretkey"
app.config["UPLOAD_FOLDER"] = "uploads"

# =============================
# DATABASE CONNECTION
# =============================
db = pymysql.connect(
    host="localhost",
    user="root",
    password="bindu541",  # 🔴 CHANGE THIS
    database="job_portal"
)

cursor = db.cursor()

# =============================
# USER SIDE
# =============================

@app.route('/')
def home():
    search = request.args.get("search")
    location = request.args.get("location")
    category = request.args.get("category")

    query = "SELECT * FROM jobs WHERE 1=1"
    values = []

    if search:
        query += " AND (title LIKE %s OR skills LIKE %s)"
        values.append(f"%{search}%")
        values.append(f"%{search}%")

    if location:
        query += " AND location = %s"
        values.append(location)

    if category:
        query += " AND category = %s"
        values.append(category)

    cursor.execute(query, tuple(values))
    jobs = cursor.fetchall()

    return render_template("index.html", jobs=jobs)


@app.route('/bookmark/<int:id>')
def bookmark(id):
    cursor.execute("INSERT INTO bookmarks (job_id) VALUES (%s)", (id,))
    db.commit()
    return redirect('/')


@app.route('/saved')
def saved():
    cursor.execute("""
        SELECT jobs.* FROM jobs
        JOIN bookmarks ON jobs.id = bookmarks.job_id
    """)
    jobs = cursor.fetchall()
    return render_template("saved.html", jobs=jobs)


@app.route('/apply/<int:id>')
def apply(id):
    return render_template("apply.html", job_id=id)


@app.route('/submit/<int:id>', methods=["POST"])
def submit(id):
    name = request.form["name"]
    email = request.form["email"]
    cover = request.form["cover"]

    file = request.files["resume"]
    filename = file.filename

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    cursor.execute("""
        INSERT INTO applications
        (job_id, name, email, resume, cover_letter)
        VALUES (%s,%s,%s,%s,%s)
    """, (id, name, email, filename, cover))

    db.commit()

    return "<h2>Application Submitted Successfully!</h2><a href='/'>Go Back</a>"


# =============================
# ADMIN SIDE
# =============================

@app.route('/admin')
def admin():
    return render_template("admin_login.html")


@app.route('/admin_login', methods=["POST"])
def admin_login():
    username = request.form["username"]
    password = request.form["password"]

    cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s",
                   (username, password))
    admin_user = cursor.fetchone()

    if admin_user:
        session["admin"] = username
        return redirect("/dashboard")
    else:
        return "<h3>Invalid Credentials</h3><a href='/admin'>Try Again</a>"


@app.route('/dashboard')
def dashboard():
    if "admin" in session:
        cursor.execute("SELECT * FROM jobs")
        jobs = cursor.fetchall()
        return render_template("admin_dashboard.html", jobs=jobs)
    else:
        return redirect("/admin")


@app.route('/add_job')
def add_job():
    if "admin" in session:
        return render_template("add_job.html")
    else:
        return redirect("/admin")


@app.route('/insert_job', methods=["POST"])
def insert_job():
    title = request.form["title"]
    company = request.form["company"]
    location = request.form["location"]
    salary = request.form["salary"]
    type = request.form["type"]
    category = request.form["category"]
    skills = request.form["skills"]
    description = request.form["description"]

    cursor.execute("""
        INSERT INTO jobs
        (title, company, location, salary, type, category, skills, description)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (title, company, location, salary, type, category, skills, description))

    db.commit()

    return redirect("/dashboard")


@app.route('/delete/<int:id>')
def delete_job(id):
    if "admin" in session:
        cursor.execute("DELETE FROM jobs WHERE id=%s", (id,))
        db.commit()
        return redirect("/dashboard")
    else:
        return redirect("/admin")


@app.route('/logout')
def logout():
    session.pop("admin", None)
    return redirect("/admin")


# =============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
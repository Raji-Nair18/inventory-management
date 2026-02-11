from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os
from datetime import datetime
from ml import predict_demand
from notify import send_email

# ---------------- APP CONFIG ----------------
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)
app.secret_key = "smartstock"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# ---------------- DATABASE ----------------
def db():
    return sqlite3.connect(DB_PATH)

from functools import wraps

def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "role" not in session or session["role"] != role:
                return redirect("/login")
            return f(*args, **kwargs)
        return wrapper
    return decorator


def init_db():
    conn = db()
    c = conn.cursor()

    # c.execute("""
    # CREATE TABLE IF NOT EXISTS users (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     name TEXT,
    #     email TEXT UNIQUE,
    #     password TEXT,
    #     role TEXT
    # )
    # """)

    # c.execute("""
    # CREATE TABLE IF NOT EXISTS products (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     name TEXT,
    #     category TEXT,
    #     stock INTEGER,
    #     expiry DATE
    # )
    # """)

    # c.execute("""
    # CREATE TABLE IF NOT EXISTS sales (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     user_id INTEGER,
    #     product_id INTEGER,
    #     date DATE
    # )
    # """)

    # c.execute("""
    # CREATE TABLE IF NOT EXISTS customers_profile (
    #     user_id INTEGER,
    #     product_id INTEGER,
    #     frequency INTEGER,
    #     PRIMARY KEY (user_id, product_id)
    # )
    # """)

    # c.execute("""
    # CREATE TABLE IF NOT EXISTS product_pairs (
    #     product_a INTEGER,
    #     product_b INTEGER,
    #     confidence REAL
    # )
    # """)

    # conn.commit()
    # conn.close()

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    c = db().cursor()
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]

    if count == 0:
        return redirect("/register")
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    conn = db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    user_count = c.fetchone()[0]

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = "admin" if user_count == 0 else request.form["role"]

        c.execute(
            "INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)",
            (name, email, password, role)
        )
        conn.commit()
        return redirect("/login")

    return render_template("register.html", first_user=(user_count == 0))

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        e = request.form["email"]
        p = request.form["password"]

        c = db().cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (e,p))
        u = c.fetchone()

        if u:
            session["id"] = u[0]
            session["role"] = u[4]
            return redirect("/" + u[4])

    return render_template("login.html")

@app.route("/admin")
@role_required("admin")
def admin():
    c = db().cursor()

    c.execute("SELECT COUNT(*) FROM products")
    total_products = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM products WHERE stock < 5")
    low_stock = c.fetchone()[0]

    c.execute("SELECT * FROM products")
    products = c.fetchall()

    return render_template(
        "admin.html",
        products=products,
        total_products=total_products,
        low_stock=low_stock
    )
@app.route("/add_product", methods=["GET", "POST"])
@role_required("admin")
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        stock = int(request.form["stock"])
        expiry = request.form["expiry"]

        conn = db()
        c = conn.cursor()
        c.execute("""
            INSERT INTO products (name, category, stock, expiry)
            VALUES (?,?,?,?)
        """, (name, category, stock, expiry))
        conn.commit()

        return redirect("/admin")

    return render_template("add_product.html")


@app.route("/customer")
def customer():
    c = db().cursor()
    c.execute("SELECT * FROM products WHERE stock > 0")
    return render_template("customer.html", products=c.fetchall())

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------- RUN ----------------
if __name__ == "__main__":
    print("📦 Using DB:", DB_PATH)
    init_db()
    app.run(debug=True)



# from flask import Flask, render_template, request, redirect, session, jsonify
# import sqlite3
# from datetime import datetime
# from ml import predict_demand
# from notify import send_email
# from notify import send_sms

# app = Flask(__name__)
# app.secret_key = "smartstock"
# DB = "database.db"

# def db():
#     return sqlite3.connect(DB)

# @app.route("/", methods=["GET","POST"])
# def login():
#     if request.method=="POST":
#         e,p = request.form["email"], request.form["password"]
#         c=db().cursor()
#         c.execute("SELECT * FROM users WHERE email=? AND password=?", (e,p))
#         u=c.fetchone()
#         if u:
#             session["id"], session["role"]=u[0],u[4]
#             return redirect(f"/{u[4]}")
#     return render_template("login.html")

# @app.route("/admin")
# def admin():
#     c=db().cursor()
#     c.execute("SELECT * FROM products")
#     return render_template("admin.html", products=c.fetchall())

# @app.route("/customer")
# def customer():
#     c=db().cursor()
#     c.execute("SELECT * FROM products WHERE stock>0")
#     return render_template("customer.html", products=c.fetchall())

# @app.route("/buy/<int:pid>")
# def buy(pid):
#     c = db().cursor()

#     c.execute("UPDATE products SET stock=stock-1 WHERE id=?", (pid,))
#     c.execute("INSERT INTO sales VALUES(NULL,?,?,?)",
#               (session["id"],pid,datetime.now().date()))

#     # 🔥 NEW LOGIC – SYNC PRODUCTS
#     c.execute("SELECT product_b FROM product_pairs WHERE product_a=?", (pid,))
#     linked = c.fetchall()

#     for (p,) in linked:
#         c.execute("SELECT stock FROM products WHERE id=?", (p,))
#         stock = c.fetchone()[0]
#         if stock < 5:
#             send_email("supplier@mail.com", f"Restock linked product {p}")

#     db().commit()
#     return redirect("/customer")

# def seasonal_factor(month, category):
#     if month in [10,11] and category=="electronics": # Diwali
#         return 1.6
#     if month in [3,4] and category=="clothes": # summer
#         return 1.3
#     return 1.0


# @app.route("/predict/<int:pid>")
# def predict(pid):
#     return jsonify(predict_demand(pid))

# app.run(debug=True)
# app.py
# from flask import Flask, render_template, request, redirect, session, jsonify
# import sqlite3
# from datetime import datetime
# from ml import predict_demand
# from notify import send_email
# from flask import Flask


# app = Flask(__name__)
# app.secret_key = "smartstock"
# import os


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DB = os.path.join(BASE_DIR, "database.db")

# def db():
#     return sqlite3.connect(DB)


# app = Flask(
#     __name__,
#     template_folder="../frontend/templates",
#     static_folder="../frontend/static"
# )

# def init_db():
#     conn = db()
#     c = conn.cursor()




# @app.route("/register", methods=["GET","POST"])
# def register():
#     c = db().cursor()
#     c.execute("SELECT COUNT(*) FROM users")
#     user_count = c.fetchone()[0]

#     if request.method == "POST":
#         name = request.form["name"]
#         email = request.form["email"]
#         password = request.form["password"]
#         role = request.form["role"]

#         # 🔐 BASIC LOGIC:
#         # First ever user → auto-admin (override role)
#         if user_count == 0:
#             role = "admin"

#         c.execute("""
#             INSERT INTO users (name,email,password,role)
#             VALUES (?,?,?,?)
#         """, (name, email, password, role))

#         db().commit()
#         return redirect("/login")

#     return render_template("register.html", first_user=(user_count == 0))


# @app.route("/")
# def home():
#     c = db().cursor()
#     c.execute("SELECT COUNT(*) FROM users")
#     user_count = c.fetchone()[0]

#     # If no users exist → force register
#     if user_count == 0:
#         return redirect("/register")

#     # Else go to login
#     return redirect("/login")

# @app.route("/login", methods=["GET","POST"])
# def login():
#     if request.method == "POST":
#         e = request.form["email"]
#         p = request.form["password"]

#         c = db().cursor()
#         c.execute(
#             "SELECT * FROM users WHERE email=? AND password=?",
#             (e, p)
#         )
#         u = c.fetchone()

#         if u:
#             session["id"] = u[0]
#             session["role"] = u[4]
#             return redirect("/" + u[4])

#     return render_template("login.html")


# @app.route("/admin")
# def admin():
#     c=db().cursor()
#     c.execute("SELECT * FROM products")
#     return render_template("admin.html", products=c.fetchall())

# @app.route("/customer")
# def customer():
#     c=db().cursor()
#     c.execute("SELECT * FROM products WHERE stock>0")
#     return render_template("customer.html", products=c.fetchall())

# @app.route("/buy/<int:pid>")
# def buy(pid):
#     c=db().cursor()

#     c.execute("UPDATE products SET stock=stock-1 WHERE id=?", (pid,))
#     c.execute("INSERT INTO sales VALUES(NULL,?,?,?)",
#               (session["id"],pid,datetime.now().date()))

#     # Track customer behavior
#     c.execute("""
#         INSERT INTO customers_profile VALUES (?,?,1)
#         ON CONFLICT(user_id,product_id)
#         DO UPDATE SET frequency=frequency+1
#     """,(session["id"],pid))

#     # Sync linked products
#     c.execute("SELECT product_b FROM product_pairs WHERE product_a=?", (pid,))
#     for (linked,) in c.fetchall():
#         c.execute("SELECT stock FROM products WHERE id=?", (linked,))
#         if c.fetchone()[0] < 5:
#             send_email("supplier@mail.com", f"Restock product {linked}")

#     db().commit()
#     return redirect("/customer")

# @app.route("/predict/<int:pid>")
# def predict(pid):
#     return jsonify(predict_demand(pid))

# if __name__ == "__main__":
#     init_db()
#     app.run(debug=True)

# app.run(debug=True)

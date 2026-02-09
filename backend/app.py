from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from datetime import datetime
from ml import predict_demand
from notify import send_email, send_sms

app = Flask(__name__)
app.secret_key = "smartstock"
DB = "database.db"

def db():
    return sqlite3.connect(DB)

@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        e,p = request.form["email"], request.form["password"]
        c=db().cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (e,p))
        u=c.fetchone()
        if u:
            session["id"], session["role"]=u[0],u[4]
            return redirect(f"/{u[4]}")
    return render_template("login.html")

@app.route("/admin")
def admin():
    c=db().cursor()
    c.execute("SELECT * FROM products")
    return render_template("admin.html", products=c.fetchall())

@app.route("/customer")
def customer():
    c=db().cursor()
    c.execute("SELECT * FROM products WHERE stock>0")
    return render_template("customer.html", products=c.fetchall())

@app.route("/buy/<int:pid>")
def buy(pid):
    c = db().cursor()

    c.execute("UPDATE products SET stock=stock-1 WHERE id=?", (pid,))
    c.execute("INSERT INTO sales VALUES(NULL,?,?,?)",
              (session["id"],pid,datetime.now().date()))

    # 🔥 NEW LOGIC – SYNC PRODUCTS
    c.execute("SELECT product_b FROM product_pairs WHERE product_a=?", (pid,))
    linked = c.fetchall()

    for (p,) in linked:
        c.execute("SELECT stock FROM products WHERE id=?", (p,))
        stock = c.fetchone()[0]
        if stock < 5:
            send_email("supplier@mail.com", f"Restock linked product {p}")

    db().commit()
    return redirect("/customer")


@app.route("/predict/<int:pid>")
def predict(pid):
    return jsonify(predict_demand(pid))

app.run(debug=True)

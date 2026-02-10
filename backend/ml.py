# ml.py
import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

def seasonal_factor(month, category):
    if month in [10,11] and category == "electronics":
        return 1.6   # Diwali
    if month in [3,4] and category == "clothes":
        return 1.3
    return 1.0

def predict_demand(pid):
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute("""
        SELECT date, COUNT(*) 
        FROM sales 
        WHERE product_id=? 
        GROUP BY date
    """,(pid,))
    data = c.fetchall()

    if len(data) < 4:
        return {"status":"Not enough data"}

    X = np.arange(len(data)).reshape(-1,1)
    y = np.array([x[1] for x in data])

    model = LinearRegression()
    model.fit(X,y)

    future = model.predict([[len(data)+7]])[0]

    c.execute("SELECT category FROM products WHERE id=?", (pid,))
    category = c.fetchone()[0]

    month = datetime.now().month
    final = future * seasonal_factor(month, category)

    return {"predicted_week_demand": int(final)}


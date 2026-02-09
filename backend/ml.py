import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_demand(pid):
    db=sqlite3.connect("database.db")
    c=db.cursor()
    c.execute("SELECT date,COUNT(*) FROM sales WHERE product_id=? GROUP BY date",(pid,))
    data=c.fetchall()
    if len(data)<3:
        return {"prediction":"Not enough data"}

    X=np.arange(len(data)).reshape(-1,1)
    y=np.array([d[1] for d in data])

    model=LinearRegression().fit(X,y)
    pred=model.predict([[len(data)+7]])[0]
    return {"predicted_next_week": int(pred)}

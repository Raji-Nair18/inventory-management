import sqlite3
from itertools import combinations
from collections import defaultdict

def generate_product_pairs():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute("SELECT user_id, date, product_id FROM sales")
    data = c.fetchall()

    baskets = defaultdict(set)
    for u,d,p in data:
        baskets[(u,d)].add(p)

    pair_count = defaultdict(int)
    item_count = defaultdict(int)

    for basket in baskets.values():
        for item in basket:
            item_count[item] += 1
        for a,b in combinations(basket,2):
            pair_count[(a,b)] += 1

    c.execute("DELETE FROM product_pairs")

    for (a,b),count in pair_count.items():
        confidence = count / item_count[a]
        if confidence > 0.5:   # threshold
            c.execute("INSERT INTO product_pairs VALUES (?,?,?)",(a,b,confidence))

    db.commit()
    db.close()

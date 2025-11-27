from flask import Flask, render_template, request, jsonify, redirect, url_for
from core.database.database import Database
import sqlite3

app = Flask(__name__)
db = Database()


def get_cursor():
    conn = sqlite3.connect(db.db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur


@app.route('/', methods=['GET'])
def index():
    conn, cur = get_cursor()
    orders = db.get_all_orders(cur)
    conn.close()

    warning = request.args.get('warning')
    return render_template('index.html', orders=orders, warning=warning)


# ==============================
#         /product 路由
# ==============================
@app.route("/product", methods=["GET", "POST", "DELETE"])
def product():

    # ---------- GET ----------
    # /product?category=飲料
    # /product?product=可口可樂
    if request.method == "GET":
        conn, cur = get_cursor()

        if "category" in request.args:
            category = request.args.get("category")
            products = db.get_product_names_by_category(cur, category)
            conn.close()
            return jsonify({"products": products})

        if "product" in request.args:
            product = request.args.get("product")
            price = db.get_product_price(cur, product)
            conn.close()
            return jsonify({"price": price})

        conn.close()
        return jsonify({"error": "Invalid GET request"}), 400

    # ---------- POST ----------
    if request.method == "POST":
        data = request.get_json()

        order_data = {
            "order_id": db.generate_order_id(),
            "product_date": data.get("date"),
            "customer_name": data.get("customer_name"),
            "product_name": data.get("product"),
            "product_amount": data.get("quantity"),
            "product_total": data.get("subtotal"),
            "product_status": data.get("status"),
            "product_note": data.get("remark")
        }

        conn, cur = get_cursor()
        db.add_order(cur, order_data)
        conn.commit()
        conn.close()

        return jsonify({"message": "新增成功"}), 200


    # ---------- DELETE ----------
    if request.method == "DELETE":
        order_id = request.args.get("order_id")
        if not order_id:
            return jsonify({"error": "order_id is required"}), 400

        conn, cur = get_cursor()
        db.delete_order(cur, order_id)
        conn.commit()
        conn.close()

        return jsonify({"message": "Order deleted successfully"}), 200
if __name__ == "__main__":
    app.run(debug=True)

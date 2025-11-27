class Database:
    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        return conn, cur

    def get_product_names_by_category(self, category):
        conn, cur = self._connect()
        cur.execute("SELECT product FROM commodity WHERE category=?", (category,))
        rows = cur.fetchall()
        conn.close()
        return [r[0] for r in rows]

    def get_product_price(self, product):
        conn, cur = self._connect()
        cur.execute("SELECT price FROM commodity WHERE product=?", (product,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None

    def add_order(self, order_data):
        conn, cur = self._connect()
        sql = """
            INSERT INTO order_list
            (order_id, date, customer_name, product, amount, total, status, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        cur.execute(sql, (
            order_data["order_id"],
            order_data["date"],
            order_data["customer_name"],
            order_data["product"],
            order_data["amount"],
            order_data["total"],
            order_data["status"],
            order_data["note"]
        ))
        conn.commit()
        conn.close()

    def delete_order(self, order_id):
        conn, cur = self._connect()
        cur.execute("DELETE FROM order_list WHERE order_id=?", (order_id,))
        conn.commit()
        conn.close()

    def get_all_orders(self):
        conn, cur = self._connect()
        sql = """
            SELECT o.order_id, o.date, o.customer_name,
                   o.product, c.price, o.amount, o.total, o.status, o.note
            FROM order_list o
            LEFT JOIN commodity c ON o.product = c.product;
        """
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows

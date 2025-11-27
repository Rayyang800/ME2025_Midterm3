import datetime
import os
import random
import sqlite3

class Database():
    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)

        # 初始化資料表（若不存在）
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # 商品表
        cur.execute("""
            CREATE TABLE IF NOT EXISTS commodity (
                category TEXT,
                product TEXT,
                price INTEGER
            );
        """)

        # 訂單表
        cur.execute("""
            CREATE TABLE IF NOT EXISTS order_list (
                order_id TEXT PRIMARY KEY,
                product_date TEXT,
                customer_name TEXT,
                product_name TEXT,
                product_amount INTEGER,
                product_total INTEGER,
                product_status TEXT,
                product_note TEXT
            );
        """)

        conn.commit()
        conn.close()

    # ------------------------------------------------------

    @staticmethod
    def generate_order_id() -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"OD{timestamp}{random_num}"

    # ------------------------------------------------------

    # 取得種類 → 商品列表
    def get_product_names_by_category(self, cur, category):
        cur.execute("SELECT product FROM commodity WHERE category=?", (category,))
        rows = cur.fetchall()
        return [r[0] for r in rows]

    # 取得商品名稱 → 單價
    def get_product_price(self, cur, product):
        cur.execute("SELECT price FROM commodity WHERE product=?", (product,))
        row = cur.fetchone()
        return row[0] if row else None

    # 新增訂單
    def add_order(self, cur, order_data):
        sql = """
            INSERT INTO order_list
            (order_id, product_date, customer_name, product_name,
             product_amount, product_total, product_status, product_note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """

        cur.execute(sql, (
            order_data["order_id"],
            order_data["product_date"],
            order_data["customer_name"],
            order_data["product_name"],
            order_data["product_amount"],
            order_data["product_total"],
            order_data["product_status"],
            order_data["product_note"]
        ))

    # 刪除訂單
    def delete_order(self, cur, order_id):
        cur.execute("DELETE FROM order_list WHERE order_id=?", (order_id,))

    # 取得所有訂單（含動態查價格）
    def get_all_orders(self, cur):
        sql = """
            SELECT 
                o.order_id, o.product_date, o.customer_name,
                o.product_name,
                c.price,
                o.product_amount,
                o.product_total,
                o.product_status,
                o.product_note
            FROM order_list o
            LEFT JOIN commodity c
                ON o.product_name = c.product;
        """
        cur.execute(sql)
        return cur.fetchall()

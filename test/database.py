import unittest
import sqlite3
from core.database.database import Database

class TestSalesDB(unittest.TestCase):
    def setUp(self):
        # 初始化 DB 實例
        self.db = Database('test_order_management.db') 
        print(self.db.db_path)

    def test_get_product_names_by_category(self):
        # 測試需求 1: 根據種類取得商品名稱
        # 這裡需要 mock 傳入的 cur，或者修改 DB class 讓他可以接受外部 connection
        # 為了方便測試同學邏輯，我們直接呼叫方法並傳入測試用的 cursor
        
        # 注意：這邊假設同學的實作是接收 (cur, category)
        # 如果有裝飾器 @BaseDB.db_operation，通常會自動處理 connection，
        # 在單元測試中我們通常會繞過裝飾器直接測邏輯，或是 Mock BaseDB。
        # 這裡示範直接傳入 self.cur 的情境
        
        results = self.db.get_product_names_by_category('主食')
        products = [r[0] for r in results]
        self.assertIn('咖哩飯', products)
        self.assertIn('蛋包飯', products)
        self.assertNotIn('鮮奶茶', products)

    def test_get_product_price(self):
        # 測試需求 2: 取得商品價格
        price = self.db.get_product_price('咖哩飯')
        self.assertEqual(price, 90)
        
        price_none = self.db.get_product_price('不存在的商品')
        self.assertIsNone(price_none)

    def test_add_and_get_order(self):
        # 測試需求 3 & 5: 新增訂單與取得訂單
        order_data = {
            'date': '2023-12-01',
            'customer_name': 'TestUser',
            'product': '咖哩飯',
            'amount': 2,
            'total': 180,
            'status': '未付款',
            'note': 'Test Note'
        }
        
        # Mock generate_order_id 因為它在 BaseDB
        self.db.generate_order_id = lambda: 'ORD-001'
        
        self.db.add_order(order_data)
        
        # 驗證是否寫入
        orders = self.db.get_all_orders()
        self.assertEqual(len(orders), 11)
        self.assertEqual(orders[-1][0], 'ORD-001') # Order ID
        self.assertEqual(orders[-1][4], 90) # 驗證是否有 JOIN 回傳單價 (index 4)
        self.assertEqual(orders[-1][5], 2)  # Amount
        self.assertEqual(orders[-1][6], 180) # Total

    def test_delete_order(self):
        # 測試需求 4: 刪除訂單
        success = self.db.delete_order('ORD-001')
        self.assertTrue(success)
        
        with sqlite3.connect('core/database/test_order_management.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM order_list WHERE order_id='ORD-001'")
            result = cur.fetchone()
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
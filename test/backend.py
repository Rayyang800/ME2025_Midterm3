import unittest
from unittest.mock import patch
from app import app 

class TestBackendAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.db') # 假設 app.py 裡面 import 了 db 物件
    def test_get_product_names(self, mock_db):
        # 測試 GET /product?category=...
        mock_db.get_product_names_by_category.return_value = ['A', 'B']
        
        response = self.app.get('/product?category=TestCat')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"product": ['A', 'B']})
        mock_db.get_product_names_by_category.assert_called_with('TestCat')

    @patch('app.db')
    def test_get_product_price(self, mock_db):
        # 測試 GET /product?product=...
        mock_db.get_product_price.return_value = 100
        
        response = self.app.get('/product?product=TestItem')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"price": 100})
        mock_db.get_product_price.assert_called_with('TestItem')

    @patch('app.db')
    def test_post_order(self, mock_db):
        # 測試 POST /product
        mock_db.add_order.return_value = True
        
        form_data = {
            'product-date': '2023-01-01',
            'customer-name': 'Client',
            'product-name': 'Item',
            'product-amount': '1',
            'product-total': '100',
            'product-status': 'Pending',
            'product-note': 'Note'
        }
        
        response = self.app.post('/product', json=form_data, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # 檢查是否呼叫了 add_order 且參數正確轉換了 key (例如 product-date -> product_date)
        args, _ = mock_db.add_order.call_args
        self.assertEqual(args[0]['customer_name'], 'Client')
        
        # 檢查是否重導向回 index (檢查 response text 包含 index 頁面的特徵，或是 warning message)
        self.assertIn(b'Order placed successfully', response.data)

    @patch('app.db')
    def test_delete_order(self, mock_db):
        # 測試 DELETE /product?order_id=...
        mock_db.delete_order.return_value = True
        
        response = self.app.delete('/product?order_id=123')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Order deleted successfully"})
        mock_db.delete_order.assert_called_with('123')

if __name__ == '__main__':
    unittest.main()
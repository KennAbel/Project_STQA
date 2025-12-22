import unittest
from models import ShoppingCart, Product

class TestShoppingCart(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()
        self.p1 = Product("Laptop", 10000000, 5)
        self.p2 = Product("Mouse", 100000, 10)

    def test_add_item(self):
        #Tes tambah barang
        self.cart.add_item(self.p1, 1)
        self.assertEqual(len(self.cart.items), 1)
        self.assertEqual(self.cart.items[0]['subtotal'], 10000000)

    def test_remove_item(self):
        #Tes hapus barang (Fitur anti-typo / case insensitive)
        self.cart.add_item(self.p1, 1)
        self.cart.remove_item("laptop") # Pakai huruf kecil harus tetap bisa hapus
        self.assertEqual(len(self.cart.items), 0)

    def test_voucher_valid(self):
        #Tes voucher diskon 50%
        self.cart.add_item(self.p1, 1) # Harga 10 Juta
        self.cart.apply_voucher("DISKON50")
        
        details = self.cart.get_details()
        
        self.assertEqual(details['subtotal'], 10000000)
        self.assertEqual(details['potongan'], 5000000) # Diskon 50%
        
        #Cek logika pajak (11% dari setelah diskon)
        #10jt - 5jt = 5jt. Pajak 11% dari 5jt = 550rb
        self.assertEqual(details['pajak'], 550000) 
        
        #Cek Total Akhir
        #5jt + 550rb = 5.550.000
        self.assertEqual(details['total'], 5550000)

    def test_voucher_invalid(self):
        #Tes voucher ngawur
        with self.assertRaises(ValueError):
            self.cart.apply_voucher("KODENGAWUR")

if __name__ == '__main__':
    unittest.main()
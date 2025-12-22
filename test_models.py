# import unittest
# from models import Product, ShoppingCart

# class TestShoppingCart(unittest.TestCase):

#     def setUp(self):
#         self.cart = ShoppingCart()
#         # Harga: 10 Juta
#         self.laptop = Product("Laptop", 10000000, 10) 
#         # Harga: 100 Ribu
#         self.mouse = Product("Mouse", 100000, 100)

#     # --- A. POSITIVE TEST ---
#     def test_add_items_sum_with_tax(self):
#         """
#         Skenario: Beli 1 Laptop (10jt) + 2 Mouse (200rb)
#         Subtotal: 10.200.000
#         Diskon: 0
#         Pajak (11%): 1.122.000
#         Total: 11.322.000
#         """
#         self.cart.add_item(self.laptop, 1)
#         self.cart.add_item(self.mouse, 2)
#         self.assertEqual(self.cart.calculate_total(), 11322000)

#     def test_voucher_50_percent_with_tax(self):
#         """
#         Skenario: Beli 1 Laptop (10jt) + Diskon 50%
#         Subtotal: 10.000.000
#         Diskon 50%: 5.000.000
#         Setelah Diskon: 5.000.000
#         Pajak (11% dari 5jt): 550.000
#         Total: 5.550.000
#         """
#         self.cart.add_item(self.laptop, 1)
#         self.cart.apply_voucher("DISKON50")
#         self.assertEqual(self.cart.calculate_total(), 5550000)

#     # --- B. NEGATIVE TEST ---
#     def test_add_negative_qty(self):
#         with self.assertRaises(ValueError):
#             self.cart.add_item(self.laptop, -1)

#     def test_invalid_voucher(self):
#         self.cart.add_item(self.laptop, 1)
#         with self.assertRaises(ValueError):
#             self.cart.apply_voucher("SALAH_BOSS")

#     # --- C. BOUNDARY TEST ---
#     def test_empty_cart(self):
#         self.assertEqual(self.cart.calculate_total(), 0)
        
#     def test_add_item_exceed_stock(self):
#         # Set stok laptop jadi 5
#         self.laptop.stok = 5
        
#         # Beli 5 (Pas) -> Berhasil
#         # Hitungan: 5 x 10jt = 50jt + PPN 11% (5.5jt) = 55.500.000
#         self.cart.add_item(self.laptop, 5)
#         self.assertEqual(self.cart.calculate_total(), 55500000)

#         # Tambah 1 lagi -> Error
#         with self.assertRaises(ValueError):
#             self.cart.add_item(self.laptop, 1)

# if __name__ == '__main__':
#     unittest.main()
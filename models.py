class Product:
    def __init__(self, nama, harga, stok):
        self.nama = nama
        self.harga = harga
        self.stok = stok

class ShoppingCart:
    def __init__(self):
        self.items = []
        self.voucher_code = None

    def add_item(self, product, qty):
        item = {
            "product": product,
            "qty": qty,
            "subtotal": product.harga * qty 
        }
        self.items.append(item)

    def remove_item(self, product_name):
        target_name = product_name.strip().lower()
        self.items = [
            item for item in self.items 
            if item['product'].nama.strip().lower() != target_name
        ]

    def apply_voucher(self, code):
        if code == "DISKON50":
            self.voucher_code = code
        else:
            raise ValueError("Kode Voucher Tidak Valid")

    def empty_cart(self):
        self.items = []
        self.voucher_code = None

    def get_details(self):
        # 1. Hitung Subtotal
        subtotal = sum(item['subtotal'] for item in self.items)
        
        # 2. Hitung Diskon
        potongan = 0
        if self.voucher_code == "DISKON50":
            potongan = subtotal * 0.50
            
        # 3. Hitung Pajak
        after_discount = subtotal - potongan
        pajak = after_discount * 0.11
        
        # 4. Hitung Total Akhir
        total = after_discount + pajak

        return {
            "subtotal": subtotal,   # HTML minta 'subtotal'
            "potongan": potongan,   # HTML minta 'potongan' (bukan discount_amount)
            "pajak": pajak,         # HTML minta 'pajak' (bukan tax)
            "total": total          # HTML minta 'total' (bukan grand_total)
        }

class User:
    def __init__(self, id, username, password, role="user"):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.cart = ShoppingCart()
        self.is_active = True
        self.is_authenticated = True
        self.is_anonymous = False

    def get_id(self):
        return self.id
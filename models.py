from flask_login import UserMixin

# Class Produk (Tetap sama)
class Product:
    def __init__(self, nama, harga, stok=100):
        self.nama = nama
        self.harga = harga
        self.stok = stok

# Class ShoppingCart (Tetap sama, logic tidak berubah)
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.discount_rate = 0.0 
        self.tax_rate = 0.11  # Pajak 11% (PPN)
        self.applied_voucher = None

    def add_item(self, product, qty):
        if qty <= 0:
            raise ValueError("Jumlah barang harus positif")
        
        current_qty_in_cart = 0
        existing_item = None
        for item in self.items:
            if item["product"].nama == product.nama:
                current_qty_in_cart = item["qty"]
                existing_item = item
                break
        
        if (current_qty_in_cart + qty) > product.stok:
            raise ValueError(f"Stok tidak cukup! Stok sisa {product.stok}.")
        
        if existing_item:
            existing_item["qty"] += qty
        else:
            self.items.append({"product": product, "qty": qty})

    def remove_item(self, product_name):
        self.items = [item for item in self.items if item["product"].nama != product_name]

    def apply_voucher(self, code):
        if code == "DISKON50":
            self.discount_rate = 0.50
            self.applied_voucher = code
        elif code == "DISKON10":
            self.discount_rate = 0.10
            self.applied_voucher = code
        else:
            raise ValueError("Kode voucher tidak valid")

    def calculate_total(self):
        # 1. Hitung Subtotal Barang
        subtotal = sum(item["product"].harga * item["qty"] for item in self.items)
        
        # 2. Hitung Potongan Diskon
        potongan = subtotal * self.discount_rate
        
        # 3. Hitung Dasar Pengenaan Pajak (Setelah Diskon)
        setelah_diskon = subtotal - potongan
        
        # 4. Hitung Pajak (11% dari harga setelah diskon)
        pajak = setelah_diskon * self.tax_rate
        
        # 5. Total Akhir
        total_akhir = setelah_diskon + pajak
        
        return int(total_akhir)

    # Helper untuk menampilkan rincian di Website (HTML)
    def get_details(self):
        subtotal = sum(item["product"].harga * item["qty"] for item in self.items)
        potongan = subtotal * self.discount_rate
        setelah_diskon = subtotal - potongan
        pajak = setelah_diskon * self.tax_rate
        total = setelah_diskon + pajak
        return {
            "subtotal": int(subtotal),
            "potongan": int(potongan),
            "pajak": int(pajak),
            "total": int(total)
        }
    
    def empty_cart(self):
        self.items = []
        self.discount_rate = 0.0
        self.applied_voucher = None

# --- NEW: Class User ---
class User(UserMixin):
    def __init__(self, id, username, password, role='user'):
        self.id = id
        self.username = username
        self.password = password
        self.role = role  # 'admin' atau 'user'
        self.cart = ShoppingCart() # Setiap user punya keranjang sendiri
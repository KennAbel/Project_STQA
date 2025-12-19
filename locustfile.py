from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        #1. Login di awal
        self.client.post("/login", data={
            "username": "budi", 
            "password": "budi123"
        })

    @task(3) #sering dilakukan (Buka Home)
    def index(self):
        self.client.get("/")

    @task(2)
    def beli_barang(self):
        # Gunakan catch_response=True agar kita bisa memanipulasi hasil test
        with self.client.get("/add/Laptop Gaming", catch_response=True) as response:
            # Cek apakah di halaman web ada tulisan "Stok tidak cukup"
            # (Sesuaikan teks ini dengan pesan error di app.py kamu)
            if "Stok tidak cukup" in response.text:
                response.failure("Gagal: Stok Habis!") # Ini akan bikin grafik jadi MERAH
            elif "Stok sisa" in response.text: # Atau validasi error lainnya
                 response.failure("Gagal: Stok Sisa!")
            else:
                response.success()

    @task(2) # Cek keranjang
    def lihat_cart(self):
        self.client.get("/cart")

    @task(1) # Testing Fitur Voucher (Baru!)
    def pakai_voucher(self):
        # Kita tes apakah server berat saat hitung diskon
        self.client.post("/apply_voucher", data={"code": "DISKON50"})

    @task(1) # Testing Checkout (Final Step)
    def checkout(self):
        # Ini akan mengosongkan keranjang
        self.client.get("/checkout")
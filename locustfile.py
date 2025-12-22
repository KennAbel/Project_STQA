from locust import HttpUser, task, between, SequentialTaskSet

# Kita buat class perilaku user yang BERURUTAN
class UserBehavior(SequentialTaskSet):
    
    # Task 1: Login
    @task
    def login(self):
        self.client.post("/login", data={
            "username": "budi", 
            "password": "budi123"
        })

    # Task 2: Lihat Home
    @task
    def index(self):
        self.client.get("/")

    # Task 3: Beli Barang (Logic Panic Buying kamu yang keren tadi)
    @task
    def beli_barang(self):
        with self.client.get("/add/Laptop Gaming", catch_response=True) as response:
            if "Stok tidak cukup" in response.text:
                response.failure("Gagal: Stok Habis!")
            elif "Stok sisa" in response.text:
                response.failure("Gagal: Stok Sisa!")
            else:
                response.success()

    # Task 4: Cek Keranjang
    @task
    def lihat_cart(self):
        self.client.get("/cart")

    # Task 5: Pakai Voucher
    @task
    def pakai_voucher(self):
        self.client.post("/apply_voucher", data={"code": "DISKON50"})

    # Task 6: Checkout & Selesai
    @task
    def checkout(self):
        self.client.get("/checkout")

# Class Utama
class WebsiteUser(HttpUser):
    # Panggil class behavior di atas
    tasks = [UserBehavior] 
    wait_time = between(1, 5) # User jeda 1-5 detik
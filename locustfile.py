from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    # Simulasi jeda antar klik user (1 sampai 5 detik)
    wait_time = between(1, 5)

    def on_start(self):
        """Dijalankan setiap kali user baru 'lahir' (Login dulu)"""
        self.client.post("/login", {
            "username": "budi",
            "password": "budi123"
        })

    @task(3) # Bobot 3: Lebih sering dilakukan
    def view_home(self):
        self.client.get("/")

    @task(1) # Bobot 1: Jarang dilakukan
    def view_cart(self):
        self.client.get("/cart")

    @task(2)
    def add_item(self):
        # Ceritanya user rajin beli Mouse
        self.client.get("/add/Mouse Wireless")
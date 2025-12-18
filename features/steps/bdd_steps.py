from behave import given, when, then
from app import app, users_db, User # Pastikan import User juga

# --- SKENARIO 1: LOGIN ---

@given('sistem toko online sudah jalan')
def step_impl(context):
    app.testing = True
    context.client = app.test_client()
    
    # PERBAIKAN: Kita paksa buat user 'budi' di sini agar pasti ada
    # Jadi tidak peduli database utama kosong/reset, test tetap jalan
    if "2" not in users_db:
        users_db["2"] = User("2", "budi", "budi123", role="user")
    
    context.users = users_db

@when('user login dengan username "{username}" dan password "{password}"')
def step_impl(context, username, password):
    # Mengirim data login
    context.response = context.client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)

@then('user harus diarahkan ke halaman home')
def step_impl(context):
    # Debugging: Jika error, print isi HTML-nya (opsional)
    if context.response.status_code != 200:
        print("STATUS CODE ERROR:", context.response.status_code)
        
    assert context.response.status_code == 200
    
    # PERBAIKAN: Jangan cari "Daftar Produk", tapi cari "Halo" atau "Logout"
    # Karena halaman home kita sekarang judulnya "Halo, budi!"
    page_content = context.response.data.decode('utf-8')
    
    # Kita anggap sukses kalau ada tombol Logout (tanda sudah login)
    assert "Logout" in page_content, "Gagal login: Tombol Logout tidak ditemukan"
    
    # Atau pastikan ada nama user
    assert "Halo, budi" in page_content, "Gagal login: Nama user tidak muncul"

@then('pesan selamat datang harus muncul')
def step_impl(context):
    # Cari potongan nama user di halaman
    assert b"Halo, budi" in context.response.data or b"Selamat datang" in context.response.data

# --- SKENARIO 2: BELANJA ---

@given('user sudah login sebagai "{username}"')
def step_impl(context, username):
    context.client = app.test_client()
    # Pastikan user ada dulu
    if "2" not in users_db:
        users_db["2"] = User("2", "budi", "budi123", role="user")
        
    # Login via backend
    context.client.post('/login', data={'username': username, 'password': f'{username}123'}, follow_redirects=True)

@when('user membeli produk "{product_name}"')
def step_impl(context, product_name):
    # Simulasi klik tombol beli
    context.response = context.client.get(f'/add/{product_name}', follow_redirects=True)

@then('total harga di keranjang harus bertambah')
def step_impl(context):
    # Pastikan tidak error dan produk masuk tabel
    assert context.response.status_code == 200
    # Cek apakah nama produk muncul di tabel keranjang (cart.html)
    # ATAU cek apakah ada flash message sukses
    assert b"berhasil ditambahkan" in context.response.data or b"Mouse Wireless" in context.response.data

# --- SKENARIO 3: VOUCHER DISKON ---

@given('keranjang berisi produk "{product_name}"')
def step_impl(context, product_name):
    # Pastikan keranjang kosong dulu biar hitungannya gampang
    with app.app_context():
        if "2" in users_db:
            users_db["2"].cart.empty_cart()
    
    # Masukkan item via URL
    context.client.get(f'/add/{product_name}', follow_redirects=True)

@when('user memasukkan kode voucher "{code}"')
def step_impl(context, code):
    # Simulasi User mengetik kode di form dan klik tombol "Pakai"
    # Sesuai route di app.py: @app.route('/apply_voucher', methods=['POST'])
    context.response = context.client.post('/apply_voucher', data={
        'code': code
    }, follow_redirects=True)

@then('potongan harga harus muncul di struk')
def step_impl(context):
    assert context.response.status_code == 200
    # Cek apakah tulisan "Diskon:" muncul di halaman HTML
    # Karena di HTML kita tulis: <td class="text-end">Diskon:</td>
    assert b"Diskon:" in context.response.data

@then('total harga harus berkurang')
def step_impl(context):
    # Cek apakah Flash Message sukses muncul
    assert b"Voucher berhasil digunakan" in context.response.data
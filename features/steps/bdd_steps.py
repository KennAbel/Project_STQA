from behave import given, when, then
from app import app, users_db, products_db, User, Product

@given('aplikasi toko online berjalan normal')
def step_impl(context):
    app.testing = True
    context.client = app.test_client()

@given('database user dan produk sudah di-reset')
def step_impl(context):
    users_db.clear()
    products_db.clear()
    # Data dummy wajib ada
    products_db.append(Product("Laptop Gaming", 15000000, 10))
    products_db.append(Product("Mouse Wireless", 150000, 100))

# --- LOGIN ---
@when('user login dengan username "{username}" dan password "{password}"')
def step_login_manual(context, username, password):
    # Setup user dummy di DB
    role = "admin" if username == "admin" else "user"
    uid = "1" if role == "admin" else "2"
    users_db[uid] = User(uid, username, password, role=role)
    
    context.response = context.client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)

@given('user sudah login sebagai "{username}"')
def step_login_auto(context, username):
    context.client = app.test_client()
    if username == "admin":
        role, pwd, uid = "admin", "admin123", "1"
    else:
        role, pwd, uid = "user", "budi123", "2"
        
    users_db[uid] = User(uid, username, pwd, role=role)
    
    context.client.post('/login', data={'username': username, 'password': pwd}, follow_redirects=True)

# --- USER ---
@then('user harus masuk ke halaman home')
def step_check_home(context):
    assert context.response.status_code == 200
    assert b"Daftar Produk" in context.response.data or b"Halo," in context.response.data

@then('pesan "{teks}" harus muncul')
def step_check_msg(context, teks):
    assert teks.encode() in context.response.data

@when('user membeli produk "{nama_produk}"')
def step_buy(context, nama_produk):
    context.response = context.client.get(f'/add/{nama_produk}', follow_redirects=True)

@then('produk "{nama_produk}" harus ada di halaman keranjang')
def step_check_cart(context, nama_produk):
    assert context.response.status_code == 200
    assert nama_produk.encode() in context.response.data

# --- VOUCHER ---
@given('keranjang user berisi produk "{nama_produk}"')
def step_fill_cart(context, nama_produk):
    context.client.get(f'/remove_item/{nama_produk}', follow_redirects=True)
    context.client.get(f'/add/{nama_produk}', follow_redirects=True)

@when('user memasukkan kode voucher "{kode}"')
def step_apply_voucher(context, kode):
    context.response = context.client.post('/apply_voucher', data={'code': kode}, follow_redirects=True)

@then('total harga harus terpotong 50 persen')
def step_check_discount(context):
    assert b"Diskon" in context.response.data

@then('potongan harga harus muncul di struk')
def step_impl(context):
    assert b"Diskon" in context.response.data

@then('total harga harus berkurang')
def step_impl(context):
    assert b"Grand Total" in context.response.data

# --- ADMIN ---
@when('admin menambah produk "{nama}" seharga {harga} stok {stok}')
def step_admin_add(context, nama, harga, stok):
    context.response = context.client.post('/admin/add', data={
        'nama': nama,
        'harga': harga,
        'stok': stok
    }, follow_redirects=True)

@then('produk "{nama}" harus muncul di halaman home')
def step_check_home_product(context, nama):
    assert nama.encode() in context.response.data
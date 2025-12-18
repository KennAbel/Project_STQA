from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import Product, ShoppingCart, User

app = Flask(__name__)
app.secret_key = 'rahasia_donk'

# --- SETUP FLASK LOGIN ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Kalau belum login, lempar ke sini

# --- DATABASE SEMENTARA (IN-MEMORY) ---
products_db = [
    Product("Laptop Gaming", 15000000, 5),
    Product("Mouse Wireless", 150000, 100),
]

# Database User (Kita isi 1 admin & 1 user default)
# Format: Dictionary biar gampang cari by ID
users_db = {
    "1": User("1", "admin", "admin123", role="admin"),
    "2": User("2", "budi", "budi123", role="user")
}

@login_manager.user_loader
def load_user(user_id):
    return users_db.get(user_id)

# --- ROUTES AUTH (LOGIN/SIGNUP) ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Cari user di database
        user = next((u for u in users_db.values() if u.username == username), None)
        
        if user and user.password == password:
            login_user(user)
            flash(f'Selamat datang, {user.username} ({user.role})!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Username atau Password salah!', 'danger')
            
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Cek apakah username sudah ada
        if any(u.username == username for u in users_db.values()):
            flash('Username sudah dipakai!', 'danger')
        else:
            # Buat ID baru (convert panjang dict ke string)
            new_id = str(len(users_db) + 1)
            # Default role adalah 'user'
            new_user = User(new_id, username, password, role='user')
            users_db[new_id] = new_user
            
            flash('Akun berhasil dibuat! Silakan login.', 'success')
            return redirect(url_for('login'))
            
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))

# --- ROUTES UTAMA ---

@app.route('/')
@login_required # Wajib login untuk lihat produk
def home():
    return render_template('index.html', products=products_db)

# --- FITUR USER (BELANJA) ---

@app.route('/add/<product_name>')
@login_required
def add_to_cart(product_name):
    selected_product = next((p for p in products_db if p.nama == product_name), None)
    if selected_product:
        try:
            # PENTING: Pakai current_user.cart, bukan cart global
            current_user.cart.add_item(selected_product, 1)
            flash(f'{product_name} ditambahkan!', 'success')
        except ValueError as e:
            flash(str(e), 'danger')
    return redirect(url_for('cart_page'))

# app.py

@app.route('/cart')
@login_required
def cart_page():
    # Ambil rincian lengkap (Dictionary)
    details = current_user.cart.get_details()
    
    # Kirim ke HTML
    return render_template('cart.html', cart=current_user.cart, details=details)

@app.route('/remove_item/<product_name>')
@login_required
def remove_from_cart(product_name):
    current_user.cart.remove_item(product_name)
    return redirect(url_for('cart_page'))

@app.route('/checkout')
@login_required
def checkout():
    current_user.cart.empty_cart()
    flash('Checkout berhasil!', 'success')
    return redirect(url_for('home'))

# --- FITUR ADMIN (CRUD) ---

@app.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add_product_page():
    # Proteksi: Hanya admin yang boleh masuk
    if current_user.role != 'admin':
        flash('Anda tidak punya akses!', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        nama = request.form.get('nama')
        try:
            harga = int(request.form.get('harga'))
            stok = int(request.form.get('stok'))
            products_db.append(Product(nama, harga, stok))
            flash('Produk berhasil ditambah.', 'success')
            return redirect(url_for('home'))
        except ValueError:
            flash('Input tidak valid', 'danger')

    return render_template('add_product.html')

@app.route('/admin/delete/<product_name>')
@login_required
def delete_product(product_name):
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    
    # Hapus produk dari list global
    global products_db
    products_db = [p for p in products_db if p.nama != product_name]
    flash(f'{product_name} telah dihapus oleh Admin.', 'warning')
    return redirect(url_for('home'))

@app.route('/admin/edit/<product_name>', methods=['GET', 'POST'])
@login_required
def edit_product(product_name):
    if current_user.role != 'admin':
        return redirect(url_for('home'))

    # Cari produk yg mau diedit
    product = next((p for p in products_db if p.nama == product_name), None)

    if request.method == 'POST':
        try:
            product.harga = int(request.form.get('harga'))
            product.stok = int(request.form.get('stok'))
            flash(f'{product.nama} berhasil diupdate!', 'success')
            return redirect(url_for('home'))
        except ValueError:
            flash('Input angka salah', 'danger')

    return render_template('edit_product.html', p=product)

# app.py (Tambahkan route ini)

@app.route('/apply_voucher', methods=['POST'])
@login_required
def apply_voucher():
    code = request.form.get('code') # Ambil tulisan dari input user
    try:
        current_user.cart.apply_voucher(code)
        flash('Voucher berhasil digunakan!', 'success')
    except ValueError as e:
        flash(str(e), 'danger') # Muncul error kalau kode salah
    return redirect(url_for('cart_page'))

if __name__ == '__main__':
    app.run(debug=True)
Feature: Website Toko Online Lengkap

  Background:
    Given aplikasi toko online berjalan normal
    And database user dan produk sudah di-reset

  # --- SKENARIO USER ---
  Scenario: User Login dan Melihat Home
    When user login dengan username "budi" dan password "budi123"
    Then user harus masuk ke halaman home
    And pesan "Halo, budi!" harus muncul

  Scenario: User Membeli Barang
    Given user sudah login sebagai "budi"
    When user membeli produk "Mouse Wireless"
    Then produk "Mouse Wireless" harus ada di halaman keranjang

  Scenario: User Menggunakan Voucher Diskon
    Given user sudah login sebagai "budi"
    And keranjang user berisi produk "Laptop Gaming"
    When user memasukkan kode voucher "DISKON50"
    Then total harga harus terpotong 50 persen
    And pesan "Voucher berhasil digunakan" harus muncul

  # --- SKENARIO ADMIN ---
  Scenario: Admin Menambah Produk Baru
    Given user sudah login sebagai "admin"
    When admin menambah produk "PlayStation 5" seharga 8000000 stok 10
    Then produk "PlayStation 5" harus muncul di halaman home
Feature: Sistem Belanja Online
  Sebagai user, saya ingin bisa login dan melihat produk

  Scenario: Login dengan password yang benar
    Given sistem toko online sudah jalan
    When user login dengan username "budi" dan password "budi123"
    Then user harus diarahkan ke halaman home
    And pesan selamat datang harus muncul

  Scenario: Menambah barang ke keranjang
    Given user sudah login sebagai "budi"
    When user membeli produk "Mouse Wireless"
    Then total harga di keranjang harus bertambah

  Scenario: Menggunakan Voucher Diskon
    Given user sudah login sebagai "budi"
    And keranjang berisi produk "Laptop Gaming"
    When user memasukkan kode voucher "DISKON50"
    Then potongan harga harus muncul di struk
    And total harga harus berkurang
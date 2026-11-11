# PRD — Sistem POS & Manajemen Coffee Shop ("educoffee")

## 1. Ringkasan dan tujuan
Aplikasi web lokal berbasis Flask dan SQLite untuk "educoffee Shop" guna mengotomatisasi pencatatan transaksi kasir, penghitungan omset harian, dan pemantauan stok bahan baku secara akurat agar meminimalkan selisih pencatatan manual.

## 2. Pengguna dan peran
* **Pemilik:** Mengakses laporan omset, mengelola data katalog menu, dan memantau ketersediaan bahan baku.
* **Kasir:** Melakukan input pesanan menu dari pelanggan, memproses pembayaran, dan melihat ringkasan struk transaksi.

## 3. Fitur (Berdasarkan Prioritas Must & Should)
### F-01 Manajemen Katalog & Transaksi Penjualan (Must, Sprint 1) <- KF-01, KF-02, KF-03, KF-04, KF-05, US-01
* **Kriteria penerimaan:**
  * Given stok biji kopi tersedia 1000 gram, When kasir mencatat penjualan 2 menu Kopi Susu, Then sistem menampilkan total harga secara otomatis dan stok biji kopi berkurang sesuai takaran resep.
  * Given stok bahan baku kosong, When kasir mencoba memproses pesanan menu tersebut, Then sistem menolak transaksi dan menampilkan pesan peringatan stok tidak cukup[cite: 14].

### F-02 Rekapitulasi Laporan Pendapatan Harian (Must, Sprint 2) <- KF-07, US-03
* **Kriteria penerimaan:**
  * Given terdapat sejumlah transaksi penjualan yang berhasil dicatat dalam satu hari, When pemilik membuka halaman laporan harian, Then sistem menampilkan total akumulasi omset secara akurat.

### F-03 Pembatasan Hak Akses Pengguna (Must, Sprint 2) <- KF-09, US-05
* **Kriteria penerimaan:**
  * Given pengguna masuk sebagai kasir, When mencoba mengakses menu pengaturan harga atau laporan keuangan utama, Then sistem menolak akses tersebut.

### F-04 Cetak Struk / Ringkasan Pembayaran (Should, Sprint 3) <- KF-06, US-02
* **Kriteria penerimaan:**
  * Given transaksi pembayaran telah selesai divalidasi, When kasir menekan tombol cetak struk, Then ringkasan teks rincian transaksi muncul di layar.

## 4. Data awal
* **Menu:** ID Menu, Nama Menu, Kategori, Harga Jual, Status Ketersediaan.
* **Transaksi:** ID Transaksi, Tanggal/Waktu, Total Harga, Daftar Item Pesanan.
* **Bahan Baku:** ID Bahan, Nama Bahan, Jumlah Stok, Satuan (gram/ml/pcs).

## 5. Di luar lingkup
* Pembacaan *barcode* fisik, aplikasi seluler terpisah, dan integrasi kurir pengantaran online[cite: 14].

## 6. Pertanyaan terbuka
* Apakah diperlukan diskon khusus atau sistem *happy hour* otomatis untuk jam-jam tertentu di kedai?
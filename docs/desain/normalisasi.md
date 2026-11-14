# Laporan Normalisasi Data — educoffee POS

## A. Analisis Data Mentah (Unnormalized Form)
Contoh lembar pencatatan atau nota transaksi awal yang digunakan di kedai:
* `no_nota`, `tanggal`, `nama_kasir`, `peran_kasir`, `daftar_item_pesanan (nama_menu, jumlah_pesanan, harga_satuan)`

## B. Tahapan Normalisasi
1. **Bentuk Normal Pertama (1NF):**
   * *Masalah:* Kolom `daftar_item_pesanan` masih berisi kelompok data berganda (*nested/repeating group*) dalam satu sel.
   * *Perbaikan:* Menguraikan setiap baris pesanan menjadi baris teratomisasi. Setiap baris kini hanya memegang satu fakta produk per nota (`NOTA_MENTAH(no_nota, tanggal, nama_kasir, peran_kasir, nama_menu, jumlah, harga_satuan)`).
2. **Bentuk Normal Kedua (2NF):**
   * *Masalah:* Atribut tanggal, nama kasir, dan peran kasir hanya bergantung pada `no_nota` (kunci sebagian), sedangkan harga dan nama menu bergantung pada identitas menu.
   * *Perbaikan:* Memecah tabel menjadi entitas terpisah: tabel **penjualan** (menyimpan informasi nota) dan tabel **menu** (menyimpan informasi produk), dihubungkan dengan tabel penghubung **detail_penjualan**.
3. **Bentuk Normal Ketiga (3NF):**
   * *Masalah:* Atribut `peran_kasir` bergantung fungsional pada `nama_kasir` (ketergantungan transitif), bukan langsung pada kunci utama nota.
   * *Perbaikan:* Memisahkan entitas **pengguna** untuk menyimpan data staf dan perannya secara mandiri, sehingga tabel penjualan cukup menyimpan kunci asing `pengguna_id`.
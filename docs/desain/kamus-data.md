# Kamus Data — Sistem POS educoffee

## 1. Tabel `pengguna`
Menyimpan data akun pihak yang mengoperasikan sistem (pemilik dan kasir).
* `id`: INTEGER, Wajib, PK, Auto-increment, Sumber (KF-09).
* `username`: TEXT, Wajib, UK, Unik untuk identitas login, Sumber (KF-09).
* `password_hash`: TEXT, Wajib, Disimpan dalam bentuk terenkripsi (*hash*), Sumber (KNF-04).
* `peran`: TEXT, Wajib, Batasan nilai: `('pemilik', 'kasir')`, Sumber (KF-09).

## 2. Tabel `barang` (Menu / Bahan Baku)
Menyimpan daftar produk menu yang dijual dan stok bahan dasarnya.
* `id`: INTEGER, Wajib, PK, Auto-increment, Sumber (KF-01).
* `nama`: TEXT, Wajib, UK, Nama menu unik, Sumber (KF-01).
* `harga_jual`: INTEGER, Wajib, Nilai $\ge 0$ (dalam Rupiah tanpa desimal), Sumber (KF-05).
* `stok`: INTEGER, Wajib, Nilai $\ge 0$ (bawaan 0), dikurangi otomatis oleh transaksi, Sumber (KF-04).
* `stok_minimum`: INTEGER, Wajib, Nilai $\ge 0$ (batas ambang peringatan stok), Sumber (KF-07).

## 3. Tabel `penjualan`
Menyimpan ringkasan kepala transaksi harian.
* `id`: INTEGER, Wajib, PK, Auto-increment, Sumber (KF-02).
* `tanggal`: TEXT, Wajib, Format tanggal ISO (`YYYY-MM-DD HH:MM:SS`), Sumber (KF-07).
* `pengguna_id`: INTEGER, Wajib, FK mengacu ke `pengguna(id)`, Sumber (KF-02).

## 4. Tabel `detail_penjualan`
Tabel penghubung relasi banyak-ke-banyak antara penjualan dan barang.
* `id`: INTEGER, Wajib, PK, Auto-increment, Sumber (KF-02).
* `penjualan_id`: INTEGER, Wajib, FK mengacu ke `penjualan(id)`, Sumber (KF-02).
* `barang_id`: INTEGER, Wajib, FK mengacu ke `barang(id)`, Sumber (KF-02).
* `jumlah`: INTEGER, Wajib, Nilai $> 0$, Sumber (KF-02).
* `harga_satuan`: INTEGER, Wajib, Nilai $\ge 0$ (harga saat transaksi terjadi), Sumber (KF-03).
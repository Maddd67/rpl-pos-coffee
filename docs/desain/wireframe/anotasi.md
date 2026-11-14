# Anotasi Wireframe — Sistem POS educoffee

## Tabel Keterangan Elemen Antarmuka Utama
| No | Elemen Halaman | Data / Aksi Terkait | Aturan / Pesan Sistem | Prinsip Antarmuka |
| :---: | :--- | :--- | :--- | :--- |
| 1 | Menu Navigasi Atas | Beranda, Penjualan, Katalog, Stok, Laporan | Konsisten di semua halaman; Menu Laporan disembunyikan untuk peran Kasir | Konsistensi |
| 2 | Input Jumlah Pesanan | `jumlah` (angka bulat) | Hanya menerima nilai angka $> 0$; Mencegah input huruf atau nilai minus | Pencegahan Galat |
| 3 | Area Pesan Galat / Peringatan | Validasi stok bahan baku | Muncul saat stok kurang: *"Stok bahan tidak mencukupi"* | Umpan Balik (KF-05) |
| 4 | Tabel Keranjang & Total | `harga_satuan`, `subtotal`, `total_harga` | Total dihitung otomatis secara *real-time*, tidak disimpan mentah | Keterbacaan |
| 5 | Tombol Aksi Utama | Simpan Penjualan / Batal | Letak tombol konfirmasi utama selalu di bagian kanan bawah formulir | Konsistensi |
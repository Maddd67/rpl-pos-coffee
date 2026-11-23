# Jurnal Vibe Coding — Proyek Edu Coffee POS

* **Nama:** Akhmad Aulia Nuur
* **NIM:** 24554010025
* **Kelompok:** Edu Coffee

| No | Tujuan | Prompt (Ringkas) | Hasil AI | Keputusan | Alasan |
| :---: | :--- | :--- | :--- | :---: | :--- |
| 1 | Kerangka proyek | Konteks: aturan-proyek + schema.sql; buat app.py, models.py, base.html | Struktur Flask dan koneksi SQLite berjalan; secret_key masih hardcoded | Ubah | Memindahkan secret_key ke variabel lingkungan (`os.environ`) demi keamanan |
| 2 | Daftar data barang | Buat rute GET /barang dan templat barang_list.html dengan status stok menipis | Halaman daftar tampil dengan kondisi kosong | Terima | Sudah sesuai wireframe dan menggunakan SQL berparameter |
| 3 | Tambah data barang | Tambahkan GET/POST /barang/tambah dengan validasi input di services.py | Validasi berjalan, tetapi pesan error belum spesifik saat nama duplikat | Ubah | Menambahkan penangkapan `sqlite3.IntegrityError` |
| 4 | Ubah data barang | Buat rute ubah data tanpa mengubah kolom stok secara langsung | Error `sqlite3.Row has no attribute get` saat render form awal | Ubah | Mengonversi objek `sqlite3.Row` menjadi `dict(barang)` |
| 5 | Hapus data barang | Tambahkan fitur hapus lewat POST dengan konfirmasi JS dan tangani FK | Berjalan sesuai harapan, GET ditolak (405) | Terima | Aman dari penghapusan tidak sengaja dan mencegah error integritas database |
| 6 | Uji keamanan dasar | Uji SQL injection dan XSS pada input nama barang | Input tersimpan sebagai teks biasa dan ter-escape otomatis oleh Jinja2 | Terima | Terbukti aman terhadap injeksi dasar |
| 7 | Tinjauan kode | Periksa seluruh diff modul CRUD dengan daftar periksa Lampiran C | Pemisahan lapisan MVC sudah bersih (tidak ada SQL di app.py) | Terima | Kode mudah dibaca dan dipahami seluruh anggota |
| 8 | [Debug] Perbaikan form ubah | Mengatasi TypeError saat membuka halaman ubah data barang | Ditemukan penyebab karena `sqlite3.Row` tidak mendukung `.get()` | Ubah | Menambahkan `dict(barang)` pada rute `ubah_barang` di `app.py` |
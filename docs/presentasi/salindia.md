# Kerangka Salindia Presentasi — Edu Coffee (v1.0.0)

1. **Judul**: Sistem Pencatatan Stok & Barang Masuk Edu Coffee (`v1.0.0`) — Identitas tim & klien.
2. **Masalah Klien**: Pencatatan stok dan bahan masuk yang rawan selisih serta kebutuhan pembatasan akses antara pemilik dan kasir.
3. **Solusi & Kebutuhan (`KF-01`–`KF-06`)**: Aplikasi web Flask + SQLite dengan dua peran (`pemilik` dan `kasir`), katalog & stok menipis, serta barang masuk.
4. **Arsitektur & Data**: Arsitektur berlapis (`app.py`, `services.py`, `models.py`) dan relasi tabel inti (`pengguna`, `barang`, `barang_masuk`) [tampilkan diagram/tangkapan layar].
5. **Alur Vibe Coding Terkendali**: Siklus spesifikasi → prompt → tinjauan → uji → keputusan (`Terima` / `Ubah` / `Tolak`) pada jurnal.
6. **Demo Bagian 1 (Peran Pemilik)**: Login `pemilik`, tambah/filter stok menipis, dan catat barang masuk hingga stok bertambah [tangkapan layar/demo langsung].
7. **Demo Bagian 2 (Peran Kasir & Keamanan)**: Login `kasir` (akses terbatas / `403` pada rute pemilik) dan verifikasi penolakan `POST` tanpa CSRF (`400`) [tangkapan layar/demo langsung].
8. **Tinjauan Kode & Keamanan**: Ringkasan temuan keamanan dan perbaikan (validasi ketat, CSRF, `SECRET_KEY` produksi, `.gitignore`).
9. **Pengujian Otomatis & Cacat**: ≥ 20 test case, pengujian `pytest` & regresi, serta perbaikan cacat `D-01`–`D-03`.
10. **UAT & Rilis `v1.0.0`**: Skenario UAT (UAT-1 s.d. UAT-5), skor SUS, triase umpan balik, server Waitress, pencadangan (`cadangkan.py`), dan tag `v1.0.0`.
11. **Analisis Jurnal Vibe Coding**: Rekap proporsi keputusan, jenis galat AI, dampak waktu (perkiraan), dan pelajaran utama.
12. **Keterbatasan & Rencana `v1.1`**: Keterbatasan rilis `1.0.0` secara jujur dan rencana tindak lanjut `v1.1`.
13. **Kontribusi Tim & Tanya Jawab**: Pembagian peran tiap anggota dan sesi tanya jawab individu tanpa bantuan AI.
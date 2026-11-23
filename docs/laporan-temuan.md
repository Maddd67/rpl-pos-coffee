# Laporan Temuan Code Review & Keamanan — Edu Coffee

### T-01 Tidak ada perlindungan token CSRF pada form POST
- Lokasi   : `app.py` dan formulir pada `templates/*.html`
- Kategori : A01 Broken Access Control
- Deskripsi: Permintaan POST (login, logout, tambah/ubah/hapus barang, tambah barang masuk) belum memvalidasi token CSRF per sesi.
- Bukti    : Mengirim POST tanpa token CSRF tetap diproses oleh rute Flask.
- Dampak   : Permintaan lintas situs dapat memicu aksi atas nama sesi pengguna yang sedang aktif.
- Risiko   : Sedang
- Perbaikan: Menambahkan `csrf_token()` per sesi, input tersembunyi di form POST, dan pemeriksaan `secrets.compare_digest` pada `before_request`.
- Status   : Diperbaiki

### T-02 Belum ada pembatasan percobaan login (rate limiting) dan log keamanan
- Lokasi   : `app.py` rute `/login` dan `@app.errorhandler(403)`
- Kategori : A07 Authentication Failures / A09 Security Logging & Alerting Failures
- Deskripsi: Percobaan login gagal berulang tidak dibatasi dan kejadian keamanan penting belum dicatat ke log.
- Bukti    : Mencoba login gagal > 5 kali berturut-turut tetap mengembalikan status normal tanpa pembatasan sementara.
- Dampak   : Memudahkan percobaan tebak kata sandi (*brute force*) dan menyulitkan audit insiden.
- Risiko   : Sedang
- Perbaikan: Menambahkan modul `percobaan.py` (batas 5 gagal per 5 menit per `IP|username`, respons `429`) serta pencatatan `logging` tanpa mencatat kata sandi.
- Status   : Diperbaiki

### T-03 Konfigurasi produksi & header keamanan HTTP dasar
- Lokasi   : `app.py` bagian konfigurasi aplikasi
- Kategori : A02 Security Misconfiguration
- Deskripsi: Belum ada penjagaan ketat saat `APP_ENV=production` tanpa `SECRET_KEY`, `SESSION_COOKIE_SECURE` belum mengikuti mode produksi, dan header keamanan dasar belum dipasang.
- Bukti    : Respons HTTP belum menyertakan `X-Content-Type-Options`, `X-Frame-Options`, dan `Referrer-Policy`.
- Dampak   : Meningkatkan risiko *clickjacking*, *MIME-sniffing*, dan kebocoran *referrer*.
- Risiko   : Rendah–Sedang
- Perbaikan: Menambahkan validasi `RuntimeError` saat produksi tanpa `SECRET_KEY`, mengatur `SESSION_COOKIE_SECURE=PRODUKSI`, mengontrol `debug` lewat `FLASK_DEBUG=1`, dan menambahkan header pada `@app.after_request`.
- Status   : Diperbaiki
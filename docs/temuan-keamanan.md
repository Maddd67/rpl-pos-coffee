# Catatan Temuan Keamanan — Edu Coffee

| No | Temuan / Catatan | Status | Rencana / Tindakan |
| :---: | :--- | :---: | :--- |
| 1 | Belum ada pembatasan percobaan login (*rate limiting*) | Ditunda (Pertemuan 12) | Evaluasi pembatasan percobaan masuk gagal pada tinjauan keamanan |
| 2 | Belum ada perlindungan token CSRF pada form POST | Ditunda (Pertemuan 12) | Tinjau dan terapkan mekanisme token CSRF sesuai standar keamanan web |
| 3 | Cookie sesi belum mengaktifkan `SESSION_COOKIE_SECURE=True` | Ditunda (Pertemuan 12) | Aktifkan saat lingkungan berjalan di atas HTTPS |
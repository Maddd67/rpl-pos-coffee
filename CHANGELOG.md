# Catatan Perubahan

Format berdasarkan [Semantic Versioning](https://semver.org/): `[versi] - tanggal`.
Bagian: **Ditambahkan**, **Diubah**, **Diperbaiki**, **Keamanan**.

## [1.0.0] - 2026-11-23
### Ditambahkan
- Autentikasi pengguna dengan peran `pemilik` dan `kasir` serta pembatasan akses per rute.
- Pengelolaan katalog menu/barang (tambah, ubah, hapus, cari, dan filter stok menipis).
- Pencatatan barang masuk dengan pembaruan stok secara otomatis.
- Skrip pencadangan basis data (`cadangkan.py`) dan tampilan versi (`v1.0.0`) di kaki halaman.

### Diperbaiki
- Penolakan input harga dengan karakter Unicode atau nilai berlebih agar tidak memicu galat 500.
- Validasi ketat format tanggal barang masuk (`TTTT-BB-HH`).

### Keamanan
- Perlindungan token CSRF pada seluruh formulir `POST`.
- Pembatasan percobaan login gagal (`429`) dan pencatatan kejadian keamanan tanpa mencatat kata sandi.
- Konfigurasi `SECRET_KEY` wajib pada mode produksi serta header keamanan HTTP dasar.
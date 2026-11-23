# Laporan Cacat — Edu Coffee

### D-01 Angka Unicode pada harga menyebabkan galat 500
- Ditemukan : 2026-11-23 oleh Tim Edu Coffee lewat uji eksploratif & `test_harga_jual`
- Langkah   : 1) Masuk sebagai pemilik. 2) Buka `/barang/tambah`. 3) Kirim `harga_jual = "²"`.
- Aktual    : `str.isdigit()` bernilai `True` untuk `"²"`, lalu `int("²")` memicu `ValueError` / galat 500.
- Diharapkan: Ditolak dengan pesan `"Harga jual harus berupa angka 0 atau lebih."` tanpa galat 500.
- Keparahan : Sedang (gagal memproses masukan khusus tanpa merusak data persisten)
- Prioritas : Sprint ini
- Penyebab  : `_bilangan()` hanya memeriksa `isdigit()` tanpa memeriksa `isascii()`.
- Perbaikan : Menambahkan `teks.isascii() and teks.isdigit()` pada `_bilangan()` di `services.py`; uji regresi: `tests/test_validasi.py::test_harga_jual`.
- Status    : Diperbaiki

### D-02 Nilai angka sangat besar melampaui batas wajar / kapasitas integer
- Ditemukan : 2026-11-23 oleh Tim Edu Coffee lewat `test_harga_jual`
- Langkah   : 1) Panggil `validasi_barang` atau `POST /barang/tambah` dengan `harga_jual = "1000000001"` atau `"9" * 30`.
- Aktual    : Tidak ada batas atas sehingga angka sangat besar tidak ditolak oleh aturan bisnis.
- Diharapkan: Ditolak karena melebihi batas atas `1.000.000.000` atau panjang maksimal 10 digit.
- Keparahan : Sedang
- Prioritas : Sprint ini
- Penyebab  : `_bilangan()` tidak membatasi panjang string dan nilai maksimum `BATAS_ANGKA`.
- Perbaikan : Menambahkan `BATAS_ANGKA = 1_000_000_000` dan batas panjang `<= 10` di `services.py`; uji regresi: `tests/test_validasi.py::test_harga_jual`.
- Status    : Diperbaiki

### D-03 Format tanggal tanpa tanda hubung diterima oleh `date.fromisoformat`
- Ditemukan : 2026-11-23 oleh Tim Edu Coffee lewat `test_tanggal_barang_masuk`
- Langkah   : 1) Kirim data barang masuk dengan `tanggal = "20261123"`.
- Aktual    : `date.fromisoformat("20261123")` diterima meskipun format spesifikasi adalah `TTTT-BB-HH`.
- Diharapkan: Ditolak dengan pesan `"Tanggal harus berformat TTTT-BB-HH."`.
- Keparahan : Rendah
- Prioritas : Nanti
- Penyebab  : `date.fromisoformat()` menerima format kompak tanpa tanda hubung.
- Perbaikan : Menambahkan pemeriksaan regex `^[0-9]{4}-[0-9]{2}-[0-9]{2}$` sebelum `date.fromisoformat()` di `services.py`; uji regresi: `tests/test_validasi.py::test_tanggal_barang_masuk`.
- Status    : Diperbaiki

## Catatan Permintaan Perubahan (Bukan Cacat)
- **PR-01**: Pembedaan nama menu/bahan baku yang hanya berbeda kapitalisasi (`"Kopi Susu"` vs `"kopi susu"`). Perilaku saat ini sesuai skema SQLite (`UNIQUE` case-sensitive); keputusan final diserahkan kepada pemilik Edu Coffee saat UAT.
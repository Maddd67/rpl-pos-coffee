# Rencana & Hasil Test Case — Edu Coffee

## 1. Matriks Keterlacakan Kebutuhan (KF)

| KF | Kebutuhan | Kriteria Penerimaan | Test Case |
| :---: | :--- | :--- | :---: |
| **KF-01** | Autentikasi masuk & keluar pengguna | Pengguna terautentikasi dapat masuk; kredensial salah ditolak dengan pesan seragam; sesi direset saat masuk/keluar | TC-18, TC-19, TC-20 |
| **KF-02** | Otorisasi peran (`pemilik` & `kasir`) | `pemilik` dapat mengelola katalog & stok masuk; `kasir` hanya melihat katalog/stok dan ditolak (`403`) pada aksi terlarang | TC-21, TC-22 |
| **KF-03** | Kelola katalog menu/barang (tambah, ubah, hapus) | Nama wajib, harga/stok/minimum bilangan bulat `0..1.000.000.000`, nama unik; hapus ditolak bila dipakai transaksi | TC-01..TC-10 |
| **KF-04** | Pencarian & filter stok menipis | Pencarian nama aman dari wildcard/SQLi; filter menipis menampilkan barang dengan `stok < stok_minimum` | TC-23, TC-24 |
| **KF-05** | Pencatatan barang masuk & pembaruan stok | Jumlah `> 0`, tanggal valid `TTTT-BB-HH`, barang ada; menambah stok secara atomik | TC-11..TC-17 |
| **KF-06** | Perlindungan CSRF & konfigurasi aman | Permintaan `POST` tanpa token CSRF ditolak (`400`) dan header keamanan dasar aktif | TC-25 |

## 2. Tabel Test Case (≥ 20 Kasus)

| ID | KF | Teknik | Masukan / Langkah | Hasil Diharapkan | Hasil Aktual | Status |
| :---: | :---: | :---: | :--- | :--- | :--- | :---: |
| TC-01 | KF-03 | BVA | `harga_jual = "0"` | Diterima (`0`) | Diterima (`0`) | Lulus |
| TC-02 | KF-03 | BVA | `harga_jual = "1"` | Diterima (`1`) | Diterima (`1`) | Lulus |
| TC-03 | KF-03 | EP | `harga_jual = "25000"` | Diterima (`25000`) | Diterima (`25000`) | Lulus |
| TC-04 | KF-03 | EP | `harga_jual = " 15000 "` | Diterima (`15000`) | Diterima (`15000`) | Lulus |
| TC-05 | KF-03 | BVA | `harga_jual = "1000000000"` | Diterima (`1000000000`) | Diterima (`1000000000`) | Lulus |
| TC-06 | KF-03 | BVA | `harga_jual = "1000000001"` | Ditolak dengan pesan harga | Ditolak dengan pesan harga | Lulus |
| TC-07 | KF-03 | Pelanggaran | `harga_jual = "-1"` | Ditolak dengan pesan harga | Ditolak dengan pesan harga | Lulus |
| TC-08 | KF-03 | Pelanggaran | `harga_jual = "²"` (Unicode) | Ditolak, bukan galat 500 | Ditolak, bukan galat 500 | Lulus |
| TC-09 | KF-03 | Normal | `nama = "Kopi Susu Gula Aren"` | Diterima | Diterima | Lulus |
| TC-10 | KF-03 | Pelanggaran | `nama = "   "` (hanya spasi) | Ditolak dengan pesan nama | Ditolak dengan pesan nama | Lulus |
| TC-11 | KF-05 | BVA | `jumlah = "1"`, tanggal `"2026-11-23"` | Diterima & stok bertambah 1 | Diterima & stok bertambah 1 | Lulus |
| TC-12 | KF-05 | BVA | `jumlah = "0"`, tanggal `"2026-11-23"` | Ditolak (`jumlah > 0`) | Ditolak (`jumlah > 0`) | Lulus |
| TC-13 | KF-05 | Pelanggaran | `jumlah = "-5"`, tanggal `"2026-11-23"` | Ditolak | Ditolak | Lulus |
| TC-14 | KF-05 | Normal | `tanggal = "2026-11-23"` | Diterima | Diterima | Lulus |
| TC-15 | KF-05 | Pelanggaran | `tanggal = "2026-02-30"` | Ditolak (tanggal tidak valid) | Ditolak (tanggal tidak valid) | Lulus |
| TC-16 | KF-05 | Pelanggaran | `tanggal = "23-11-2026"` | Ditolak (format salah) | Ditolak (format salah) | Lulus |
| TC-17 | KF-05 | Pelanggaran | `tanggal = "20261123"` | Ditolak (harus `TTTT-BB-HH`) | Ditolak (harus `TTTT-BB-HH`) | Lulus |
| TC-18 | KF-01 | BVA | `username` 3 huruf, sandi 8 karakter | Valid (`[]`) | Valid (`[]`) | Lulus |
| TC-19 | KF-01 | BVA | `username` 2 huruf / sandi 7 karakter | Ditolak (`galat` tidak kosong) | Ditolak (`galat` tidak kosong) | Lulus |
| TC-20 | KF-01 | BVA | `username` 30 huruf vs 31 huruf | 30 valid, 31 ditolak | 30 valid, 31 ditolak | Lulus |
| TC-21 | KF-02 | Pelanggaran | `kasir` mengakses `GET /barang/tambah` | Status `403` | Status `403` | Lulus |
| TC-22 | KF-02 | Pelanggaran | `kasir` mengirim `POST /barang/1/hapus` | Status `403`, data utuh | Status `403`, data utuh | Lulus |
| TC-23 | KF-04 | Normal | Filter `status=menipis` saat stok `< minimum` | Menampilkan barang menipis saja | Menampilkan barang menipis saja | Lulus |
| TC-24 | KF-04 | Pelanggaran | Cari nama `"100%"` & `' OR 1=1 --` | Cocok literal, tanpa SQLi | Cocok literal, tanpa SQLi | Lulus |
| TC-25 | KF-06 | Pelanggaran | `POST /login` tanpa `csrf_token` | Status `400` | Status `400` | Lulus |
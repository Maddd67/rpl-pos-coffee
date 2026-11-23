# Rencana User Acceptance Test (UAT) — Edu Coffee

Tujuan      : Memastikan pemilik dan kasir Edu Coffee dapat menjalankan alur kerja harian (kelola menu/bahan baku, pantau stok menipis, catat barang masuk, serta hak akses peran) pada aplikasi.
Peserta     : Pemilik Edu Coffee (peran `pemilik`), Kasir Edu Coffee (peran `kasir`); Pengamat: Anggota Tim Edu Coffee.
Tanggal     : Minggu 14 (sesuai konfirmasi jadwal klien)   Tempat: Edu Coffee   Durasi: 60 menit
Lingkungan  : Aplikasi Flask + SQLite lokal dengan basis data uji karangan, akun uji `pemilik` dan `kasir` (tanpa data pribadi nyata).
Kriteria lulus: Seluruh skenario utama lulus, tidak ada cacat Kritis atau Tinggi yang terbuka, dan klien menyetujui hasil pengujian.

| ID | KF | Skenario (Bahasa Klien) | Langkah | Hasil Diharapkan | Lulus? | Catatan |
| :---: | :---: | :--- | :--- | :--- | :---: | :--- |
| UAT-1 | KF-01 | Masuk dan keluar dari akun kerja | 1) Buka halaman login. 2) Isi nama pengguna & kata sandi lalu klik Masuk. 3) Klik Keluar. | Berhasil masuk ke katalog; setelah Keluar kembali ke halaman login. | | |
| UAT-2 | KF-03 | Menambah menu atau bahan baku baru | 1) Masuk sebagai pemilik. 2) Klik `+ Tambah barang`. 3) Isi nama, harga jual, stok awal, dan stok minimum lalu Simpan. | Barang baru muncul di tabel katalog beserta stok dan statusnya. | | |
| UAT-3 | KF-05 | Mencatat kiriman bahan baku masuk | 1) Masuk sebagai pemilik. 2) Buka `Barang masuk` → `+ Catat barang masuk`. 3) Pilih barang, isi jumlah & tanggal lalu Simpan. | Riwayat barang masuk bertambah dan stok barang naik sesuai jumlah. | | |
| UAT-4 | KF-04 | Memeriksa bahan baku yang stoknya menipis | 1) Buka `Katalog & Stok`. 2) Centang `Stok menipis saja` lalu klik Cari. | Hanya barang dengan stok di bawah batas minimum yang tampil. | | |
| UAT-5 | KF-02 | Kasir mencoba mengakses fitur khusus pemilik | 1) Masuk sebagai kasir. 2) Periksa menu & coba akses `/barang/tambah` atau `/masuk`. | Tombol kelola tidak muncul dan akses langsung ditolak (`403`). | | |

Cara merekam temuan: Pengamat mencatat hasil tiap skenario selama sesi UAT; temuan ketidaksesuaian dimasukkan ke `docs/pengujian/laporan-cacat.md` sebagai cacat atau permintaan perubahan.
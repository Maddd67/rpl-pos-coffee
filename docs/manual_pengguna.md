#### **C. `docs/manual-pengguna.md`**
```markdown
# Manual Pengguna — Edu Coffee (v1.0.0)

Panduan ini disusun untuk **pemilik** dan **kasir** Edu Coffee menggunakan data contoh karangan.

## 1. Masuk dan Keluar Aplikasi
1. Buka alamat aplikasi di peramban (misalnya `http://127.0.0.1:8000` atau alamat jaringan toko yang ditentukan).
2. Isi **Nama pengguna** dan **Kata sandi**, lalu klik **Masuk**.
3. Untuk mengakhiri sesi, klik tombol **Keluar** di pojok kanan atas.

![Halaman masuk Edu Coffee](gambar/01-login.png)

## 2. Melihat, Mencari, dan Memfilter Stok Menipis
1. Buka menu **Katalog & Stok**.
2. Ketik nama menu atau bahan baku pada kotak **Cari nama barang**, lalu klik **Cari**.
3. Centang **Stok menipis saja** lalu klik **Cari** untuk melihat barang yang jumlah stoknya di bawah batas minimum.
4. Klik **Atur ulang** untuk menampilkan seluruh daftar kembali.

![Daftar katalog dan status stok](gambar/02-katalog-stok.png)

## 3. Menambah, Mengubah, dan Menghapus Barang (Khusus Pemilik)
1. Masuk menggunakan akun **pemilik**.
2. Klik **+ Tambah barang**, isi **Nama**, **Harga jual (Rp)**, **Stok awal**, dan **Stok minimum**, lalu klik **Simpan**.
3. Untuk mengubah data, klik **Ubah** pada baris barang terkait, perbarui isian, lalu klik **Simpan**.
4. Untuk menghapus barang yang belum dipakai transaksi, klik **Hapus** dan konfirmasi.

![Form tambah atau ubah barang](gambar/03-form-barang.png)

## 4. Mencatat Barang Masuk (Khusus Pemilik)
1. Masuk menggunakan akun **pemilik**.
2. Buka menu **Barang masuk** pada navigasi atas.
3. Pilih **Barang**, isi **Jumlah** (angka lebih dari 0) dan **Tanggal** (`TTTT-BB-HH`), lalu klik **Simpan**.
4. Stok barang pada katalog akan bertambah otomatis sesuai jumlah yang dicatat.

![Form pencatatan barang masuk](gambar/04-barang-masuk.png)

## 5. Bila Ada Masalah
| Gejala / Pesan yang Muncul | Langkah Mengatasi |
| :--- | :--- |
| **"Nama pengguna atau kata sandi salah."** | Periksa kembali penulisan nama pengguna dan kata sandi; jika lupa, hubungi pemilik akun. |
| **"Terlalu banyak percobaan gagal. Coba lagi beberapa menit lagi."** | Tunggu beberapa menit sebelum mencoba masuk kembali. |
| **"Akses ditolak"** | Akun Anda tidak memiliki hak akses untuk fitur tersebut (fitur kelola barang/barang masuk khusus `pemilik`). |
| **Pesan merah di bawah isian form** | Periksa aturan isian (misalnya jumlah harus lebih dari 0 atau tanggal sesuai format), perbaiki, lalu klik **Simpan** lagi. |
| **Halaman tidak terbuka di peramban** | Pastikan komputer/server aplikasi menyala dan terhubung ke jaringan yang sama. |
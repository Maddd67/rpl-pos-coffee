# Rencana Pengujian — educoffee POS

## 1. Tujuan dan Ruang Lingkup
Menguji seluruh fitur fungsional utama berprioritas **Must** dan **Should** (`KF-01` sampai dengan `KF-09`).

## 2. Strategi Pengujian
* **Uji Black-Box Manual:** Berbasis kriteria penerimaan (*Given-When-Then*) pada PRD dan skenario use case.
* **Uji Otomatis Dasar:** Pengujian logika inti basis data menggunakan skrip Python (`tests/cek_skema.py`).
* **Uji Penerimaan Pengguna (UAT):** Demonstrasi langsung bersama klien nyata (PT dan BM).

## 3. Lingkungan dan Data Uji
* Perangkat: Laptop operasional kasir / peramban web standar.
* Data: Menggunakan data karangan tiruan (*mock data*), bebas dari informasi data pribadi asli.

## 4. Daftar Test Case (Pengujian Fungsional)
| ID | KF | Prasyarat / Data Uji | Langkah Pengujian | Hasil Diharapkan | Teknik Uji |
| :---: | :---: | :--- | :--- | :--- | :--- |
| TC-01 | KF-04 | Stok biji kopi = 1000g; Jual = 200g | Kasir memilih menu kopi dan memasukkan jumlah 200g | Transaksi tersimpan; Stok biji kopi tersisa 800g | Partisi Valid |
| TC-02 | KF-05 | Stok biji kopi = 100g; Jual = 150g | Kasir mencoba memproses pesanan 150g | Ditolak sistem; Muncul pesan *"Stok bahan tidak mencukupi"* | Nilai Batas (Di atas) |
| TC-03 | KF-05 | Stok biji kopi = 100g; Jual = 100g | Kasir mencoba memproses pesanan tepat 100g | Transaksi berhasil; Stok biji kopi tersisa 0 | Nilai Batas (Tepat) |
| TC-04 | KF-05 | Stok biji kopi = 100g; Jual = 0 atau -5 | Kasir memasukkan jumlah pesanan bernilai 0 atau minus | Ditolak sistem; Tampil peringatan *"Jumlah pesanan tidak valid"* | Partisi Tidak Valid |
| TC-05 | KF-09 | Akun Kasir valid (username & password benar) | Masuk melalui halaman login sistem | Berhasil masuk ke halaman beranda sesuai hak akses kasir | Partisi Valid |
| TC-06 | KF-09 | Akun Kasir mencoba akses halaman Laporan Owner | Kasir menavigasi langsung ke halaman laporan omset | Akses ditolak atau menu tersembunyi (*Role-based access*) | Hak Akses |

## 5. Matriks Keterlacakan Kebutuhan — Test Case
| KF / Kebutuhan | Use Case | Halaman Terkait | Prioritas | Test Case |
| :---: | :---: | :--- | :---: | :---: |
| KF-01 | UC-05 | wf-03 Daftar Katalog Menu | Must | TC-07 |
| KF-02 | UC-01 | wf-02 Catat Penjualan | Must | TC-01 |
| KF-05 | UC-01 | wf-02 Catat Penjualan | Must | TC-02, TC-03, TC-04 |
| KF-09 | UC-03 | wf-01 Login & Beranda | Must | TC-05, TC-06 |
# SRS Ringkas — Sistem POS & Manajemen Coffee Shop ("educoffee")

## 1. Pendahuluan
* **Tujuan dan ruang lingkup:** Dokumen ini mendefinisikan spesifikasi kebutuhan perangkat lunak aplikasi berbasis web lokal untuk pengelolaan kasir (POS) dan stok bahan baku pada "KopiKita Coffee Shop". Ruang lingkup mencakup katalog menu, pencatatan transaksi penjualan, pemantauan stok bahan baku, dan rekapitulasi laporan harian bagi pemilik. Di luar lingkup mencakup program loyalitas pelanggan (*membership points*), integrasi pembayaran digital pihak ketiga yang kompleks, dan layanan pesan-antar online.
* **Definisi/istilah:** POS (*Point of Sale*), *Peak Hours* (jam sibuk kedai), *Must Have*, *Should Have*.

## 2. Gambaran umum
* **Pengguna dan peran:** 
  * *Pemilik (Owner):* Mengelola data menu, memantau laporan omset, dan mengawasi stok. Kurang terbiasa dengan antarmuka teknis yang rumit.
  * *Kasir:* Melakukan input pesanan dan memproses pembayaran transaksi harian. Membutuhkan antarmuka yang cepat dan mudah dipahami dalam beberapa kali ketukan.
* **Lingkungan operasi:** Berjalan pada peramban web lokal menggunakan server Flask dan penyimpanan database SQLite, diakses melalui laptop standar di area kasir. Kondisi jaringan internet kedai kadang tidak stabil.
* **Batasan:** Waktu pengerjaan proyek terbatas hingga Minggu 16; anggaran perangkat terbatas (hanya menggunakan laptop operasional yang tersedia di kedai); kemampuan literasi digital pengguna dasar.
* **Asumsi (dengan rencana konfirmasi):** 
  * Transaksi pembayaran tunai dan QRIS manual dicatat dalam satu sistem terpusat tanpa perlu koneksi API perbankan langsung (Rencana konfirmasi: ditanyakan saat kunjungan klien).
  * Batas minimum peringatan stok bahan baku ditetapkan seragam 5 unit untuk setiap jenis bahan utama (Rencana konfirmasi: dikonfirmasi ke bagian stok/pemilik).

## 3. Kebutuhan fungsional

| ID | Pernyataan Kebutuhan | Sumber | Prioritas | Asumsi? |
| :---: | :--- | :---: | :---: | :---: |
| KF-01 | Sistem harus menampilkan daftar menu minuman dan makanan beserta harga dan kategorinya. | US-01 | Must | Tidak |
| KF-02 | Sistem harus mencatat pesanan pelanggan ke dalam keranjang transaksi aktif. | US-01 | Must | Tidak |
| KF-03 | Sistem harus menghitung total harga tagihan transaksi secara otomatis. | US-01 | Must | Tidak |
| KF-04 | Sistem harus mengurangi stok bahan baku secara otomatis ketika transaksi penjualan berhasil dicatat. | US-01 | Must | Tidak |
| KF-05 | Sistem harus menolak transaksi penjualan apabila stok bahan baku tidak mencukupi dan menampilkan pesan peringatan[cite: 14]. | US-01 | Must | Tidak |
| KF-06 | Sistem harus mencetak atau menampilkan ringkasan struk bukti pembayaran transaksi[cite: 14]. | US-02 | Should | Tidak |
| KF-07 | Sistem harus merekapitulasi total pendapatan omset penjualan harian secara otomatis[cite: 14]. | US-03 | Must | Tidak |
| KF-08 | Sistem harus menampilkan daftar bahan baku yang berada di bawah batas minimum stok[cite: 14]. | US-04 | Should | Tidak |
| KF-09 | Sistem harus membatasi hak akses pengelolaan harga menu hanya kepada akun pemilik[cite: 14]. | US-05 | Must | Tidak |
| KF-10 | Sistem harus menyediakan fitur penambahan variasi kustomisasi rasa (misal: tingkat es atau gula)[cite: 14]. | US-06 | Could | Ya |

* **Alasan MoSCoW:** Proporsi *Must Have* diatur sekitar 60% dari total fitur utama agar target pengembangan selesai tepat waktu dalam 4 Sprint.

## 4. Kebutuhan non-fungsional

| ID | Kategori | Pernyataan Terukur | Sumber |
| :---: | :--- | :--- | :--- |
| KNF-01 | Kinerja | Halaman pencatatan transaksi penjualan harus terbuka dalam waktu $\le$ 3 detik pada laptop klien[cite: 14]. | Catatan wawancara |
| KNF-02 | Keandalan | Sistem harus dapat dioperasikan secara lokal tanpa memerlukan koneksi internet aktif[cite: 14]. | Catatan wawancara |
| KNF-03 | Kegunaan | Kasir baru harus dapat menyelesaikan pencatatan satu transaksi tanpa bantuan setelah demonstrasi selama 5 menit[cite: 14]. | Catatan wawancara |
| KNF-04 | Keamanan | Kata sandi akun pemilik harus disimpan dalam bentuk terenkripsi (*hash*) di dalam basis data[cite: 14]. | Asumsi |

## 5. Di luar lingkup (Won't have)
* Integrasi mesin pembaca *barcode* fisik.
* Aplikasi seluler (*mobile app*) berbasis Android/iOS terpisah.
* Fitur pengiriman pesanan kurir daring (*online delivery*).
* *Alasan:* Keterbatasan perangkat keras klien, anggaran, dan durasi waktu pengerjaan proyek[cite: 14].

## 6. Matriks keterlacakan
| User Story | KF / KNF Turunan | Uji (diisi Minggu 13) |
| :--- | :--- | :--- |
| US-01 (Pencatatan Pesanan) | KF-01, KF-02, KF-03, KF-04, KF-05 | [Akan diisi] |
| US-02 (Struk Pembayaran) | KF-06, KNF-01 | [Akan diisi] |
| US-03 (Laporan Omset) | KF-07 | [Akan diisi] |
| US-04 (Peringatan Stok) | KF-08 | [Akan diisi] |
| US-05 (Hak Akses) | KF-09, KNF-04 | [Akan diisi] |

## Riwayat konfirmasi klien
| Tanggal | Tanggapan | Perubahan |
| :--- | :--- | :--- |
| [Tanggal Konfirmasi] | Disetujui oleh pemilik kedai dengan catatan penambahan tombol cetak struk cepat. | Memasukkan KF-06 ke prioritas *Should Have*. |
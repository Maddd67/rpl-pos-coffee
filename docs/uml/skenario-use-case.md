# Skenario Use Case — Sistem POS Coffee Shop ("educoffee")

## UC-01 Catat Penjualan
* **Aktor:** Kasir
* **KF terkait:** KF-01, KF-02, KF-03, KF-04, KF-05
* **Prasyarat:** Kasir sudah masuk (*login*) ke dalam sistem.

### Alur utama
1. Kasir membuka halaman menu dan memilih produk kopi atau makanan yang dipesan pelanggan.
2. Kasir memasukkan jumlah pesanan untuk setiap produk.
3. Sistem memeriksa ketersediaan stok bahan baku di basis data[cite: 15].
4. Sistem menghitung total harga tagihan secara otomatis dan menampilkan rincian keranjang[cite: 15].
5. Kasir mengonfirmasi pembayaran dan sistem menyimpan data transaksi, lalu mengurangi stok bahan baku terkait[cite: 15].

### Alur alternatif
* 2a. Kasir mengubah jumlah pesanan atau menghapus menu dari keranjang sebelum pembayaran dikonfirmasi; sistem memperbarui total tagihan secara otomatis.

### Pengecualian
* 3a. Jika jumlah bahan baku tidak mencukupi, sistem menampilkan pesan peringatan "Stok bahan tidak mencukupi" dan transaksi gagal disimpan[cite: 15].

### Pascakondisi
* Transaksi penjualan tersimpan di sistem dan stok bahan baku berkurang sesuai takaran resep[cite: 15].

---

## UC-02 Rekapitulasi Laporan Harian
* **Aktor:** Pemilik
* **KF terkait:** KF-07
* **Prasyarat:** Pemilik sudah masuk ke dalam sistem dengan akun hak akses khusus.

### Alur utama
1. Pemilik memilih menu laporan pada bilah navigasi utama.
2. Sistem mengambil data seluruh transaksi yang berhasil dicatat pada hari tersebut.
3. Sistem menghitung akumulasi total pendapatan dan menampilkan ringkasan omset harian di layar.

### Alur alternatif
* 2a. Pemilik memilih rentang tanggal tertentu; sistem menampilkan rekapitulasi sesuai periode yang dipilih.

### Pengecualian
* 2b. Jika tidak ada transaksi pada tanggal tersebut, sistem menampilkan pesan "Belum ada data transaksi pada periode ini".

### Pascakondisi
* Laporan omset harian berhasil ditampilkan kepada pemilik.

---

## UC-03 Manajemen Hak Akses Pengguna
* **Aktor:** Pemilik
* **KF terkait:** KF-09
* **Prasyarat:** Pemilik sudah masuk ke dalam sistem.

### Alur utama
1. Pemilik mengakses menu manajemen hak akses atau pengaturan akun.
2. Pemilik menambah atau memperbarui data akun staf kasir beserta peran aksesnya.
3. Sistem menyimpan perubahan data peran pengguna tersebut.

### Pengecualian
* 1a. Jika akun dengan peran kasir mencoba mengakses halaman pengaturan harga atau laporan keuangan utama, sistem menolak akses dan menampilkan peringatan "Akses ditolak".

### Pascakondisi
* Hak akses peran pengguna berhasil diperbarui di sistem.

---

## UC-04 Cetak Struk Pembayaran
* **Aktor:** Kasir
* **KF terkait:** KF-06
* **Prasyarat:** Transaksi penjualan telah sukses divalidasi dan disimpan oleh sistem.

### Alur utama
1. Setelah transaksi berhasil, kasir menekan tombol "Cetak Struk" pada layar konfirmasi.
2. Sistem merender data rincian transaksi (nama kedai, daftar menu, jumlah, harga, dan total).
3. Sistem mengirimkan perintah cetak ke perangkat penampil atau pencetak struk.

### Pengecualian
* 3a. Jika perangkat cetak tidak terhubung, sistem menampilkan pesan "Gagal mencetak struk, periksa koneksi perangkat".

### Pascakondisi
* Ringkasan struk berhasil ditampilkan atau dicetak sebagai bukti pembayaran sah.

---

## UC-05 Manajemen Katalog Menu
* **Aktor:** Pemilik
* **KF terkait:** KF-01
* **Prasyarat:** Pemilik sudah masuk ke dalam sistem.

### Alur utama
1. Pemilik membuka menu pengelolaan katalog produk.
2. Pemilik memasukkan atau memperbarui informasi produk (nama menu, kategori, harga jual, dan status).
3. Sistem memvalidasi input data dan menyimpannya ke dalam katalog menu kedai.

### Pengecualian
* 2a. Jika ada kolom wajib yang dikosongkan, sistem menampilkan pesan kesalahan "Mohon lengkapi seluruh data menu".

### Pascakondisi
* Katalog menu di sistem diperbarui dan langsung tampil pada halaman kasir.
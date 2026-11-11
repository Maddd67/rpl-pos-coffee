# Daftar User Story — educoffee POS

## US-01 Pencatatan Transaksi Penjualan Kasir
* **Sebagai** kasir,
* **saya ingin** mencatat menu kopi yang dipesan pelanggan beserta jumlahnya,
* **agar** total tagihan otomatis dihitung dan stok bahan berkurang secara sistem.
* **Kriteria Penerimaan:**
  * Given stok biji kopi robusta tersedia 1000 gram dan harga Kopi Susu Rp18.000, When kasir memasukkan 2 pesanan Kopi Susu dan menekan tombol bayar, Then sistem menampilkan total Rp36.000 dan stok biji kopi berkurang sesuai takaran resep.
  * Given kasir memilih menu dengan stok bahan baku kosong, When kasir mencoba memproses pesanan, Then sistem menolak transaksi dan menampilkan peringatan "Stok bahan tidak mencukupi".
* **Sumber:** Catatan wawancara narasumber kasir no. 03.
* **[Asumsi: tidak]**

## US-02 Laporan Rekapitulasi Omset Harian
* **Sebagai** pemilik coffee shop,
* **saya ingin** melihat ringkasan total pendapatan penjualan harian pada halaman dashboard,
* **agar** saya dapat memantau omset harian tanpa harus merekap nota manual.
* **Kriteria Penerimaan:**
  * Given terdapat 10 transaksi sukses pada tanggal hari ini dengan total Rp500.000, When pemilik membuka menu laporan harian, Then sistem menampilkan total omset sebesar Rp500.000 dalam waktu $\le$ 3 detik.
* **Sumber:** Catatan wawancara narasumber pemilik no. 01.
* **[Asumsi: tidak]**
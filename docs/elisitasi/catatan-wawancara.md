# Catatan Wawancara — Sistem POS & Manajemen Coffee Shop ("educoffee")

* **Tanggal / Lokasi:** [11-11-2026] / Kedai educoffee, Sampit
* **Narasumber:** Pengelola / Pemilik Usaha (Peran: Pemilik & Kasir)
* **Pewawancara / Pencatat:** Tim Pengembang R.P.L. (Mahasiswa D3 TI)

---

## A. Catatan Wawancara (Simulasi / Nyata)

| No | Pertanyaan | Jawaban Ringkas | Fakta / Asumsi | Konfirmasi? |
| :---: | :--- | :--- | :--- | :---: |
| 1 | Cara catat pesanan saat ramai? | Kasir menulis manual di nota kertas rangkap dua; satu untuk dapur, satu untuk arsip kasir. | Fakta | Tidak |
| 2 | Proses cek ketersediaan bahan baku? | Bagian stok mengecek fisik barang secara manual ke gudang setiap pagi sebelum toko buka. | Fakta | Tidak |
| 3 | Kendala pencatatan keuangan? | Sering ada selisih uang kas di laci dengan jumlah rekap nota kertas akibat salah hitung manual. | Fakta | Tidak |
| 4 | Seberapa sering kehabisan bahan? | Kurang lebih 2 kali dalam sebulan untuk susu segar dan cup ukuran tertentu. | Fakta | Ya |
| 5 | Dokumen yang rutin diisi? | Buku nota penjualan fisik dan buku tulis kecil untuk catatan sisa bahan baku gudang. | Fakta | Tidak |
| 6 | Perangkat di area kasir? | Tersedia 1 unit laptop lama milik pemilik dan 1 unit ponsel pintar untuk pembayaran QRIS. | Fakta | Tidak |
| 7 | Harapan fitur utama? | Pemilik ingin laporan omset harian bisa direkap otomatis tanpa harus menghitung nota satu per satu. | Fakta | Tidak |

---

## B. Analisis Pernyataan (Fakta vs Solusi vs Kebutuhan)

| Pernyataan dari Catatan | Jenis | Kebutuhan di Baliknya |
| :--- | :--- | :--- |
| "Saya ingin aplikasi kasir di laptop yang ada tombol gambar menunya." | Solusi | Kasir memerlukan antarmuka menu berbasis web/desktop yang visual dan cepat diakses untuk mempercepat proses input pesanan. |
| "Tolong buatkan rekap omset harian agar saya tidak perlu lembur hitung nota." | Kebutuhan | Sistem harus menyediakan fitur rekapitulasi laporan pendapatan harian dan bulanan secara otomatis dan akurat. |
| "Stok biji kopi harus bisa terpantau otomatis supaya tidak kehabisan." | Kebutuhan | Sistem harus mengurangi stok bahan baku secara otomatis setiap kali transaksi penjualan produk berhasil diproses. |
| "Kasir tidak boleh mengubah harga menu sembarangan." | Kebutuhan | Sistem harus menerapkan pembatasan hak akses (*role-based access control*), di mana hanya pemilik yang dapat mengubah data harga menu. |
| "Harus bisa dipakai meskipun internet kadang lambat." | Kebutuhan | Sistem harus dirancang andal dan efisien dalam penggunaan jaringan lokal maupun koneksi internet terbatas. |
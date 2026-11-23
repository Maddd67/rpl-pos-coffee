# Jurnal Vibe Coding — Edu Coffee

| No | Tujuan | Prompt | Hasil AI | Keputusan | Alasan |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | Konfigurasi `TOKO_DB` & `versi.py` | Minta penyesuaian path DB dari env dan konstanta `VERSI` | Memberikan konfigurasi env dan `VERSI = "1.0.0"` | Terima | Sesuai kebutuhan rilis dan lulus uji [Galat: lainnya — tanpa galat, perlu verifikasi env] |
| 2 | [Debug] Validasi barang masuk | Minta validasi jumlah > 0 dan tanggal `TTTT-BB-HH` | Menyarankan parsing tanggal dan cek jumlah positif | Ubah | Ditambah penolakan format tidak valid dan uji kasus batas [Galat: aturan-bisnis] |
| 3 | [Keamanan] Penyimpanan sandi & sesi | Minta konfigurasi keamanan sesi produksi | Menyarankan opsi tambahan di luar kebutuhan rilis awal | Tolak | Disesuaikan agar tetap fokus pada `SECRET_KEY` dan cookie sesi [Galat: di-luar-lingkup] |
```[cite: 8]

Setelah berkas-berkas pada `jurnal/` siap, jalankan `python alat/analisis_jurnal.py jurnal/*.md` untuk mengecek rekap keputusan, jenis galat AI, serta memastikan tidak ada peringatan format[cite: 8].
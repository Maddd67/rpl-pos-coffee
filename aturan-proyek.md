# Aturan Proyek untuk Asisten AI

## Stack
* Python 3.14 (minimal kompatibel dengan 3.10), Flask, SQLite[cite: 14].
* Penambahan pustaka/paket pihak ketiga eksternal hanya diperbolehkan setelah mendapatkan persetujuan kelompok[cite: 14].

## Struktur folder
* `app.py` (Titik masuk utama aplikasi Flask)
* `templates/` (Kumpulan berkas tampilan HTML)
* `static/` (Berkas aset pendukung seperti CSS/gambar)
* `tests/` (Berkas pengujian sistem)
* `docs/` (Dokumentasi proyek termasuk SRS dan elisitasi)[cite: 14]

## Konvensi
* Komentar kode dan teks antarmuka (*UI*) menggunakan **Bahasa Indonesia**[cite: 14].
* Terapkan aturan satu fitur per *commit*, gunakan nama fungsi yang deskriptif dan mudah dipahami[cite: 14].

## Larangan
* Jangan menambahkan paket dependensi baru tanpa izin eksplisit[cite: 14].
* Jangan menaruh kata sandi, token, atau kunci rahasia (*secret keys*) di dalam kode program[cite: 14].
* Ubah atau edit hanya berkas yang diminta secara spesifik oleh pengembang; jangan menghapus atau melemahkan pengujian yang ada[cite: 14].

## Menjalankan dan menguji
* Jalankan perintah: `python app.py` di terminal lokal[cite: 14].
* Pengujian otomatis (*automated testing*) akan ditambahkan pada tahap selanjutnya (Minggu 13)[cite: 14].
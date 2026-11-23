# Edu Coffee — Sistem Pencatatan Stok & Barang Masuk

Aplikasi web berbasis Flask dan SQLite untuk membantu pemilik dan kasir **Edu Coffee** mengelola katalog menu/bahan baku, memantau stok menipis, dan mencatat barang masuk.

Versi saat ini: **1.0.0** (lihat [CHANGELOG.md](CHANGELOG.md)).

## Fitur
- Login multi-peran: **pemilik** (kelola barang & barang masuk) dan **kasir** (lihat serta cari katalog & stok).
- Kelola barang: tambah, ubah, hapus, pencarian nama, dan filter stok menipis.
- Barang masuk: mencatat stok masuk dan memperbarui jumlah stok barang.
- Pencadangan basis data ke folder `cadangan/`.

## Kebutuhan
- Python 3.10 atau lebih baru
- Git

## Instalasi
```powershell
git clone [https://github.com/Maddd67/rpl-pos-coffee.git](https://github.com/Maddd67/rpl-pos-coffee.git)
cd rpl-pos-coffee
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
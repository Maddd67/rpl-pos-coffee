"""Uji regresi cepat Edu Coffee: jalankan `python tests/uji_cepat.py` dari folder proyek."""
import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import models

models.DB_PATH = Path(tempfile.mkdtemp()) / "uji_educoffee.db"
import app as aplikasi

c = aplikasi.app.test_client()


def kirim(url, **data):
    return c.post(url, data=data, follow_redirects=True)


def ada(teks, hasil):
    assert teks in hasil.text, f"Tidak ditemukan: {teks!r}"


# --- Modul barang ---
ada("Belum ada barang", c.get("/barang"))
for n, h, s, m in [
    ("Kopi Arabika", 25000, 10, 5),
    ("Susu Segar", 18000, 3, 10),
    ("Diskon 100%", 15000, 1, 5),
]:
    ada(
        "berhasil ditambahkan",
        kirim("/barang/tambah", nama=n, harga_jual=h, stok=s, stok_minimum=m),
    )

ada(
    "sudah ada",
    kirim("/barang/tambah", nama="Kopi Arabika", harga_jual=20000, stok=2, stok_minimum=5),
)
ada(
    "berhasil diubah",
    kirim("/barang/1/ubah", nama="Kopi Arabika", harga_jual=27000, stok_minimum=5),
)
assert models.ambil_barang(1)["stok"] == 10

# --- Pencarian dan penyaringan ---
hasil = c.get("/barang?q=arab")
ada("Kopi Arabika", hasil)
assert "Susu Segar" not in hasil.text

hasil = c.get("/barang?status=menipis")
ada("Susu Segar", hasil)
assert "Kopi Arabika" not in hasil.text

hasil = c.get("/barang?q=%25")
ada("Diskon 100%", hasil)
assert "Kopi Arabika" not in hasil.text

ada("Tidak ada barang yang cocok", c.get("/barang?q=' OR 1=1 --"))

# --- Modul barang masuk (relasi & transaksi) ---
ada("Belum ada barang masuk", c.get("/masuk"))
ada(
    "stok bertambah",
    kirim("/masuk/tambah", barang_id=2, jumlah=20, tanggal="2026-11-23"),
)
assert models.ambil_barang(2)["stok"] == 23
ada(
    "lebih dari 0",
    kirim("/masuk/tambah", barang_id=2, jumlah=-3, tanggal="2026-11-23"),
)
ada(
    "Barang tidak ditemukan",
    kirim("/masuk/tambah", barang_id=999, jumlah=5, tanggal="2026-11-23"),
)
ada(
    "Pilih barang",
    kirim("/masuk/tambah", barang_id="", jumlah=5, tanggal="2026-11-23"),
)
ada(
    "TTTT-BB-HH",
    kirim("/masuk/tambah", barang_id=2, jumlah=5, tanggal="23-11-2026"),
)
assert models.ambil_barang(2)["stok"] == 23
assert len(models.semua_barang_masuk()) == 1

# --- Kunci asing ---
ada("tidak dapat dihapus", kirim("/barang/2/hapus"))
assert c.get("/barang/2/hapus").status_code == 405

# --- Uji atomisitas transaksi ---
try:
    models.tambah_barang_masuk(999, 5, "2026-11-23")
except sqlite3.IntegrityError:
    pass
assert len(models.semua_barang_masuk()) == 1

print("SEMUA UJI LULUS")
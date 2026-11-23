"""Uji regresi cepat Edu Coffee: jalankan `python tests/uji_cepat.py` dari folder proyek."""
import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import models

models.DB_PATH = Path(tempfile.mkdtemp()) / "uji_educoffee.db"
import app as aplikasi
import services

c = aplikasi.app.test_client()


def login_sebagai(username, password):
    return c.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )


def logout():
    return c.post("/logout", follow_redirects=True)


def kirim(url, **data):
    return c.post(url, data=data, follow_redirects=True)


def ada(teks, hasil):
    assert teks in hasil.text, f"Tidak ditemukan: {teks!r}"


# --- Tamu diarahkan ke login ---
resp_tamu = c.get("/barang", follow_redirects=False)
assert resp_tamu.status_code == 302
assert "/login" in resp_tamu.headers["Location"]

# --- Pembuatan akun & hash kata sandi ---
assert services.buat_pengguna("owner_edu", "SandiOwner123", "pemilik") == []
assert services.buat_pengguna("kasir_edu", "SandiKasir123", "kasir") == []

baris_owner = models.cari_pengguna("owner_edu")
assert baris_owner is not None
assert baris_owner["password_hash"] != "SandiOwner123"
assert baris_owner["password_hash"].startswith(("scrypt:", "pbkdf2:"))

# --- Pesan login sama untuk sandi salah & pengguna tidak ada ---
gagal_sandi = c.post(
    "/login",
    data={"username": "owner_edu", "password": "SalahPassword"},
    follow_redirects=True,
)
gagal_user = c.post(
    "/login",
    data={"username": "tidak_ada_user", "password": "SalahPassword"},
    follow_redirects=True,
)
assert "Nama pengguna atau kata sandi salah." in gagal_sandi.text
assert "Nama pengguna atau kata sandi salah." in gagal_user.text

# --- Pencegahan open redirect ---
resp_next = c.post(
    "/login?next=https://jahat.example",
    data={"username": "owner_edu", "password": "SandiOwner123"},
    follow_redirects=False,
)
assert resp_next.status_code == 302
assert not resp_next.headers["Location"].startswith("https://jahat.example")

# --- Login sebagai pemilik & uji CRUD + pencarian + relasi ---
res_login = login_sebagai("owner_edu", "SandiOwner123")
ada("Belum ada barang", res_login)

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

ada("tidak dapat dihapus", kirim("/barang/2/hapus"))
assert c.get("/barang/2/hapus").status_code == 405

try:
    models.tambah_barang_masuk(999, 5, "2026-11-23")
except sqlite3.IntegrityError:
    pass
assert len(models.semua_barang_masuk()) == 1

# --- Logout & uji otorisasi peran kasir (403) ---
logout()
resp_setelah_logout = c.get("/barang", follow_redirects=False)
assert resp_setelah_logout.status_code == 302
assert "/login" in resp_setelah_logout.headers["Location"]

res_kasir = login_sebagai("kasir_edu", "SandiKasir123")
ada("Kopi Arabika", res_kasir)

assert c.get("/barang/tambah").status_code == 403
assert c.get("/masuk").status_code == 403
assert c.post("/barang/1/hapus").status_code == 403
assert models.ambil_barang(1) is not None

logout()
print("SEMUA UJI LULUS")
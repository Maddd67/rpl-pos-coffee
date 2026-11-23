import re
from datetime import date

from werkzeug.security import check_password_hash, generate_password_hash

import models

PERAN = ("pemilik", "kasir")
_HASH_PALSU = generate_password_hash("bukan-kata-sandi-sungguhan-educoffee")


def _bilangan(teks):
    """Ubah teks menjadi bilangan bulat >= 0, atau None bila tidak valid."""
    teks = (teks or "").strip()
    return int(teks) if teks.isdigit() else None


def validasi_barang(form, dengan_stok=True):
    """Validasi input menu/bahan baku Edu Coffee sesuai kamus data."""
    galat = []
    nama = (form.get("nama") or "").strip()
    harga = _bilangan(form.get("harga_jual"))
    minimum = _bilangan(form.get("stok_minimum"))
    stok = _bilangan(form.get("stok")) if dengan_stok else 0

    if not nama:
        galat.append("Nama barang wajib diisi.")
    if harga is None:
        galat.append("Harga jual harus berupa angka 0 atau lebih.")
    if minimum is None:
        galat.append("Stok minimum harus berupa angka 0 atau lebih.")
    if stok is None:
        galat.append("Stok awal harus berupa angka 0 atau lebih.")

    data = {
        "nama": nama,
        "harga_jual": harga,
        "stok_minimum": minimum,
        "stok": stok,
    }
    return data, galat


def validasi_barang_masuk(form):
    """Validasi masukan form barang masuk untuk Edu Coffee."""
    galat = []
    barang_id = _bilangan(form.get("barang_id"))
    jumlah = _bilangan(form.get("jumlah"))
    tanggal = (form.get("tanggal") or "").strip()

    if barang_id is None:
        galat.append("Pilih barang terlebih dahulu.")
    if not jumlah:
        galat.append("Jumlah harus berupa angka lebih dari 0.")
    try:
        date.fromisoformat(tanggal)
    except ValueError:
        galat.append("Tanggal harus berformat TTTT-BB-HH.")

    return {"barang_id": barang_id, "jumlah": jumlah, "tanggal": tanggal}, galat


def validasi_pengguna_baru(username, password, peran):
    """Validasi akun baru: username 3-30 alfanumerik/garis bawah, sandi >= 8 karakter."""
    galat = []
    if not re.fullmatch(r"[A-Za-z0-9_]{3,30}", username or ""):
        galat.append("Nama pengguna 3-30 karakter: huruf, angka, atau garis bawah.")
    if len(password or "") < 8:
        galat.append("Kata sandi minimal 8 karakter.")
    if peran not in PERAN:
        galat.append("Peran harus pemilik atau kasir.")
    return galat


def buat_pengguna(username, password, peran):
    """Simpan pengguna Edu Coffee dengan kata sandi ter-hash."""
    bersih_username = (username or "").strip()
    galat = validasi_pengguna_baru(bersih_username, password, peran)
    if not galat:
        models.tambah_pengguna(bersih_username, generate_password_hash(password), peran)
    return galat


def autentikasi(username, password):
    """Verifikasi kredensial dan kembalikan baris pengguna bila cocok, selain itu None."""
    pengguna = models.cari_pengguna((username or "").strip())
    hash_tersimpan = pengguna["password_hash"] if pengguna else _HASH_PALSU
    cocok = check_password_hash(hash_tersimpan, password or "")
    return pengguna if (pengguna and cocok) else None
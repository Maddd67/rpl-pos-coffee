"""Uji partisi ekuivalen dan nilai batas pada services.py."""
import pytest

import services


def _form_barang(**ubah):
    form = {
        "nama": "Kopi Susu",
        "harga_jual": "18000",
        "stok": "10",
        "stok_minimum": "3",
    }
    form.update(ubah)
    return form


@pytest.mark.parametrize("harga, diharapkan_valid, nilai_diharapkan", [
    ("0", True, 0),                    # TC-01 BVA batas bawah
    ("1", True, 1),                    # TC-02 BVA di atas batas bawah
    ("25000", True, 25000),            # TC-03 EP valid
    (" 15000 ", True, 15000),          # TC-04 EP spasi pinggir
    ("1000000000", True, 1000000000),  # TC-05 BVA batas atas
    ("1000000001", False, None),       # TC-06 BVA di atas batas atas
    ("-1", False, None),               # TC-07 Pelanggaran negatif
    ("²", False, None),                # TC-08 Pelanggaran angka Unicode
    ("9" * 30, False, None),           # Pelanggaran panjang berlebih
])
def test_harga_jual(harga, diharapkan_valid, nilai_diharapkan):
    data, galat = services.validasi_barang(_form_barang(harga_jual=harga))
    assert (len(galat) == 0) is diharapkan_valid
    if diharapkan_valid:
        assert data["harga_jual"] == nilai_diharapkan


@pytest.mark.parametrize("nama, diharapkan_valid", [
    ("Kopi Susu Gula Aren", True),     # TC-09 Normal
    ("   ", False),                    # TC-10 Pelanggaran spasi
    ("", False),                       # Pelanggaran kosong
])
def test_nama_barang(nama, diharapkan_valid):
    _, galat = services.validasi_barang(_form_barang(nama=nama))
    assert (len(galat) == 0) is diharapkan_valid


@pytest.mark.parametrize("jumlah, diharapkan_valid", [
    ("1", True),                       # TC-11 BVA batas bawah valid
    ("0", False),                      # TC-12 BVA nol ditolak
    ("-5", False),                     # TC-13 Pelanggaran negatif
])
def test_jumlah_barang_masuk(jumlah, diharapkan_valid):
    form = {"barang_id": "1", "jumlah": jumlah, "tanggal": "2026-11-23"}
    _, galat = services.validasi_barang_masuk(form)
    assert (len(galat) == 0) is diharapkan_valid


@pytest.mark.parametrize("tanggal, diharapkan_valid", [
    ("2026-11-23", True),              # TC-14 Normal
    ("2026-02-30", False),             # TC-15 Pelanggaran tanggal mustahil
    ("23-11-2026", False),             # TC-16 Pelanggaran urutan
    ("20261123", False),               # TC-17 Pelanggaran tanpa tanda hubung
])
def test_tanggal_barang_masuk(tanggal, diharapkan_valid):
    form = {"barang_id": "1", "jumlah": "5", "tanggal": tanggal}
    _, galat = services.validasi_barang_masuk(form)
    assert (len(galat) == 0) is diharapkan_valid


@pytest.mark.parametrize("username, sandi, diharapkan_valid", [
    ("abc", "12345678", True),         # TC-18 BVA batas bawah
    ("ab", "12345678", False),         # TC-19 BVA username 2 karakter
    ("abc", "1234567", False),         # TC-19 BVA sandi 7 karakter
    ("a" * 30, "12345678", True),      # TC-20 BVA username 30 karakter
    ("a" * 31, "12345678", False),     # TC-20 BVA username 31 karakter
])
def test_pengguna_baru(username, sandi, diharapkan_valid):
    galat = services.validasi_pengguna_baru(username, sandi, "kasir")
    assert (len(galat) == 0) is diharapkan_valid
"""Uji alur HTTP, akumulasi stok barang masuk, matriks akses peran, dan CSRF."""
import pytest

import models

MATRIKS_AKSES = [
    ("GET", "/barang", 302, 200, 200),
    ("GET", "/barang/tambah", 302, 403, 200),
    ("GET", "/masuk", 302, 403, 200),
    ("GET", "/masuk/tambah", 302, 403, 200),
]


def test_tambah_barang_lalu_tampil_di_daftar(pemilik, kirim):
    resp = kirim(
        pemilik,
        "/barang/tambah",
        nama="Espresso",
        harga_jual="15000",
        stok="12",
        stok_minimum="4",
    )
    assert resp.status_code == 200
    assert "Barang berhasil ditambahkan." in resp.text
    assert "Espresso" in resp.text


def test_barang_masuk_menambah_stok_terakumulasi(pemilik, kirim):
    kirim(
        pemilik,
        "/barang/tambah",
        nama="Biji Kopi House Blend",
        harga_jual="45000",
        stok="5",
        stok_minimum="3",
    )
    barang_id = models.cari_barang("House Blend")[0]["id"]
    kirim(pemilik, "/masuk/tambah", barang_id=str(barang_id), jumlah="10", tanggal="2026-11-23")
    kirim(pemilik, "/masuk/tambah", barang_id=str(barang_id), jumlah="5", tanggal="2026-11-23")
    assert models.ambil_barang(barang_id)["stok"] == 20


@pytest.mark.parametrize("metode, path, status_tamu, status_kasir, status_pemilik", MATRIKS_AKSES)
def test_matriks_akses_rute(tamu, kasir, pemilik, metode, path, status_tamu, status_kasir, status_pemilik):
    assert tamu.open(path, method=metode).status_code == status_tamu
    assert kasir.open(path, method=metode).status_code == status_kasir
    assert pemilik.open(path, method=metode).status_code == status_pemilik


def test_kasir_ditolak_hapus_dan_post_tanpa_csrf_ditolak_400(kasir, pemilik, kirim):
    kirim(
        pemilik,
        "/barang/tambah",
        nama="Matcha Latte",
        harga_jual="22000",
        stok="8",
        stok_minimum="2",
    )
    barang_id = models.cari_barang("Matcha Latte")[0]["id"]
    assert kirim(kasir, f"/barang/{barang_id}/hapus", ikuti=False).status_code == 403
    assert pemilik.post(f"/barang/{barang_id}/hapus", data={}).status_code == 400
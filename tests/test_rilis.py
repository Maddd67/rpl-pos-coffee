"""Uji kesiapan rilis: format versi, tampilan versi, CHANGELOG, .gitignore, requirements, dan cadangan."""
import re
import sqlite3
from pathlib import Path

import cadangkan
from versi import VERSI

AKAR = Path(__file__).resolve().parent.parent


def test_versi_berformat_semver():
    assert re.fullmatch(r"\d+\.\d+\.\d+", VERSI)


def test_versi_tampil_di_halaman(tamu):
    assert f"v{VERSI}" in tamu.get("/login").text


def test_changelog_memuat_versi_rilis():
    isi_changelog = (AKAR / "CHANGELOG.md").read_text(encoding="utf-8")
    assert f"## [{VERSI}]" in isi_changelog


def test_gitignore_mengecualikan_rahasia_dan_data():
    baris = (AKAR / ".gitignore").read_text(encoding="utf-8").splitlines()
    for entri in (".env", "cadangan/"):
        assert entri in baris


def test_requirements_dikunci_versinya():
    for baris in (AKAR / "requirements.txt").read_text(encoding="utf-8").splitlines():
        teks = baris.strip()
        if teks and not teks.startswith("#"):
            assert "==" in teks, teks


def test_cadangan_berisi_data_yang_sama(pemilik, kirim, tmp_path):
    kirim(
        pemilik,
        "/barang/tambah",
        nama="Kopi Susu Gula Aren",
        harga_jual="18000",
        stok="15",
        stok_minimum="5",
    )
    berkas_cadangan = cadangkan.cadangkan(tmp_path)
    koneksi = sqlite3.connect(berkas_cadangan)
    try:
        baris = koneksi.execute("SELECT nama, stok FROM barang").fetchall()
        assert baris == [("Kopi Susu Gula Aren", 15)]
    finally:
        koneksi.close()
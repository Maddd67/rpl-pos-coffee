"""Uji pertama pytest untuk memverifikasi validasi dasar barang."""
import services


def test_validasi_harga_nol_tanpa_galat():
    data, galat = services.validasi_barang({
        "nama": "Air Mineral",
        "harga_jual": "0",
        "stok": "10",
        "stok_minimum": "2",
    })
    assert galat == []
    assert data["harga_jual"] == 0
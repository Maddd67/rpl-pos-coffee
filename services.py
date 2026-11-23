from datetime import date


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
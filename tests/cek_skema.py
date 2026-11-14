import sqlite3

db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys = ON")
db.executescript(open("docs/desain/schema.sql", encoding="utf-8").read())

tabel = [r[0] for r in db.execute(
    "SELECT name FROM sqlite_master WHERE type='table' "
    "AND name NOT LIKE 'sqlite_%' ORDER BY name")]
print("Tabel terdeteksi:", ", ".join(tabel))

# Uji pelanggaran batasan (Harus ditolak oleh SQLite)
UJI = [
    ("stok negatif pada barang", "INSERT INTO barang(nama, harga_jual, stok) VALUES ('Kopi Hitam', 15000, -5)"),
    ("peran di luar pilihan valid", "INSERT INTO pengguna(username, password_hash, peran) VALUES ('budi', 'hash123', 'kurir')"),
    ("FK penjualan mengacu kasir fiktif", "INSERT INTO penjualan(tanggal, pengguna_id) VALUES ('2026-11-14 10:00:00', 999)"),
    ("jumlah detail penjualan nol atau negatif", "INSERT INTO detail_penjualan(penjualan_id, barang_id, jumlah, harga_satuan) VALUES (1, 1, 0, 15000)"),
]

for ket, sql in UJI:
    try:
        db.execute(sql)
        print("GAGAL (seharusnya ditolak):", ket)
    except sqlite3.Error as e:
        print("OK ditolak:", ket, "->", e)
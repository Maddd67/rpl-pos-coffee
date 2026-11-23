import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).with_name("educoffee.db")
SCHEMA = Path(__file__).parent / "docs" / "desain" / "schema.sql"


@contextmanager
def koneksi():
    """Buka koneksi SQLite, aktifkan kunci asing, lalu commit dan tutup."""
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    try:
        yield db
        db.commit()
    finally:
        db.close()


def init_db():
    """Buat basis data Edu Coffee dari schema.sql bila belum ada."""
    if not DB_PATH.exists():
        with koneksi() as db:
            db.executescript(SCHEMA.read_text(encoding="utf-8"))


def semua_barang():
    with koneksi() as db:
        return db.execute("SELECT * FROM barang ORDER BY nama").fetchall()


def ambil_barang(barang_id):
    with koneksi() as db:
        return db.execute("SELECT * FROM barang WHERE id = ?", (barang_id,)).fetchone()


def tambah_barang(nama, harga_jual, stok, stok_minimum):
    with koneksi() as db:
        db.execute(
            "INSERT INTO barang (nama, harga_jual, stok, stok_minimum) VALUES (?, ?, ?, ?)",
            (nama, harga_jual, stok, stok_minimum),
        )


def ubah_barang(barang_id, nama, harga_jual, stok_minimum):
    with koneksi() as db:
        db.execute(
            "UPDATE barang SET nama = ?, harga_jual = ?, stok_minimum = ? WHERE id = ?",
            (nama, harga_jual, stok_minimum, barang_id),
        )


def hapus_barang(barang_id):
    with koneksi() as db:
        db.execute("DELETE FROM barang WHERE id = ?", (barang_id,))
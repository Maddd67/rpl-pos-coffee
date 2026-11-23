import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(os.environ.get("TOKO_DB") or Path(__file__).resolve().parent / "educoffee.db")
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


def _escape_like(teks):
    """Netralkan % dan _ agar dicari sebagai huruf biasa."""
    return teks.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def cari_barang(kata="", hanya_menipis=False):
    """Ambil daftar barang; opsional disaring nama dan status stok menipis."""
    sql = "SELECT * FROM barang WHERE nama LIKE ? ESCAPE '\\'"
    param = ["%" + _escape_like(kata) + "%"]
    if hanya_menipis:
        sql += " AND stok < stok_minimum"
    sql += " ORDER BY nama"
    with koneksi() as db:
        return db.execute(sql, param).fetchall()


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


def tambah_barang_masuk(barang_id, jumlah, tanggal):
    """Catat barang masuk dan tambah stok dalam satu transaksi atomik."""
    with koneksi() as db:
        db.execute(
            "INSERT INTO barang_masuk (barang_id, jumlah, tanggal) VALUES (?, ?, ?)",
            (barang_id, jumlah, tanggal),
        )
        db.execute(
            "UPDATE barang SET stok = stok + ? WHERE id = ?",
            (jumlah, barang_id),
        )


def semua_barang_masuk():
    with koneksi() as db:
        return db.execute(
            "SELECT m.id, m.tanggal, b.nama AS nama_barang, m.jumlah "
            "FROM barang_masuk m "
            "JOIN barang b ON b.id = m.barang_id "
            "ORDER BY m.tanggal DESC, m.id DESC"
        ).fetchall()


def tambah_pengguna(username, password_hash, peran):
    with koneksi() as db:
        db.execute(
            "INSERT INTO pengguna (username, password_hash, peran) VALUES (?, ?, ?)",
            (username, password_hash, peran),
        )


def cari_pengguna(username):
    with koneksi() as db:
        return db.execute(
            "SELECT * FROM pengguna WHERE username = ?",
            (username,),
        ).fetchone()


def ambil_pengguna(pengguna_id):
    with koneksi() as db:
        return db.execute(
            "SELECT * FROM pengguna WHERE id = ?",
            (pengguna_id,),
        ).fetchone()
        
def tambah_barang_masuk(barang_id, jumlah, tanggal):
    with koneksi() as db:
        db.execute(
            "INSERT INTO barang_masuk (barang_id, jumlah, tanggal) VALUES (?, ?, ?)",
            (barang_id, jumlah, tanggal),
        )
        db.execute(
            "UPDATE barang SET stok = stok + ? WHERE id = ?",
            (jumlah, barang_id),
        )
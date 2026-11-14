PRAGMA foreign_keys = ON;

CREATE TABLE pengguna (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  username      TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  peran         TEXT NOT NULL CHECK (peran IN ('pemilik', 'kasir'))
);

CREATE TABLE barang (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  nama         TEXT NOT NULL UNIQUE,
  harga_jual   INTEGER NOT NULL CHECK (harga_jual >= 0),
  stok         INTEGER NOT NULL DEFAULT 0 CHECK (stok >= 0),
  stok_minimum INTEGER NOT NULL DEFAULT 0 CHECK (stok_minimum >= 0)
);

CREATE TABLE penjualan (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  tanggal     TEXT NOT NULL,
  pengguna_id INTEGER NOT NULL REFERENCES pengguna(id)
);

CREATE TABLE detail_penjualan (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  penjualan_id INTEGER NOT NULL REFERENCES penjualan(id),
  barang_id    INTEGER NOT NULL REFERENCES barang(id),
  jumlah       INTEGER NOT NULL CHECK (jumlah > 0),
  harga_satuan INTEGER NOT NULL CHECK (harga_satuan >= 0)
);
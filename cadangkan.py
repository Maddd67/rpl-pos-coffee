"""Cadangkan basis data Edu Coffee: python cadangkan.py [folder_tujuan]."""
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import models


def cadangkan(folder=None):
    """Salin basis data aktif ke folder cadangan memakai SQLite backup API."""
    folder = Path(folder) if folder else Path(__file__).resolve().parent / "cadangan"
    folder.mkdir(parents=True, exist_ok=True)
    berkas = folder / f"educoffee-{datetime.now():%Y%m%d-%H%M%S}.db"
    sumber = sqlite3.connect(models.DB_PATH)
    tujuan = sqlite3.connect(berkas)
    try:
        with tujuan:
            sumber.backup(tujuan)
    finally:
        sumber.close()
        tujuan.close()
    return berkas


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    print("Cadangan dibuat:", cadangkan(target))
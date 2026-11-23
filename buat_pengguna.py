"""Buat akun awal Edu Coffee: python buat_pengguna.py"""
import getpass
import sqlite3

import models
import services


def main():
    models.init_db()
    username = input("Nama pengguna: ").strip()
    peran = input("Peran (pemilik/kasir): ").strip()
    password = getpass.getpass("Kata sandi (min. 8 karakter): ")
    try:
        galat = services.buat_pengguna(username, password, peran)
    except sqlite3.IntegrityError:
        galat = ["Nama pengguna sudah dipakai."]
    print("\n".join(galat) if galat else "Akun Edu Coffee berhasil dibuat.")


if __name__ == "__main__":
    main()
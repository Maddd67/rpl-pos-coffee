"""Pembatasan percobaan login Edu Coffee (penyimpanan dalam memori per proses)."""
import time

BATAS = 5
JENDELA = 300  # detik (5 menit)

_gagal = {}


def _bersihkan(kunci, sekarang):
    _gagal[kunci] = [t for t in _gagal.get(kunci, []) if sekarang - t < JENDELA]


def terkunci(kunci, sekarang=None):
    sekarang = time.monotonic() if sekarang is None else sekarang
    _bersihkan(kunci, sekarang)
    return len(_gagal[kunci]) >= BATAS


def catat_gagal(kunci, sekarang=None):
    sekarang = time.monotonic() if sekarang is None else sekarang
    _bersihkan(kunci, sekarang)
    _gagal[kunci].append(sekarang)


def reset(kunci):
    _gagal.pop(kunci, None)
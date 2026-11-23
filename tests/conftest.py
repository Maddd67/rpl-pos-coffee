"""Fixture bersama pytest untuk Edu Coffee menggunakan basis data sementara."""
import sys
import tempfile
from pathlib import Path

import pytest
from werkzeug.security import generate_password_hash

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import models

models.DB_PATH = Path(tempfile.mkdtemp()) / "uji_educoffee.db"
import app as aplikasi
import percobaan

SANDI_PEMILIK = "SandiPemilik123"
SANDI_KASIR = "SandiKasir123"


@pytest.fixture(autouse=True)
def basis_bersih():
    """Reset basis data sementara dan status pembatasan login sebelum tiap uji."""
    models.DB_PATH.unlink(missing_ok=True)
    models.init_db()
    percobaan._gagal.clear()
    hash_cepat = lambda s: generate_password_hash(s, method="pbkdf2:sha256:1000")
    models.tambah_pengguna("pemilik_edu", hash_cepat(SANDI_PEMILIK), "pemilik")
    models.tambah_pengguna("kasir_edu", hash_cepat(SANDI_KASIR), "kasir")


@pytest.fixture
def kirim():
    """Kirim permintaan POST dengan token CSRF yang sah untuk sesi klien uji."""
    def _kirim(client, url, ikuti=True, **data):
        with client.session_transaction() as s:
            s.setdefault("csrf_token", "token-uji-pytest")
            token = s["csrf_token"]
        data.setdefault("csrf_token", token)
        return client.post(url, data=data, follow_redirects=ikuti)
    return _kirim


@pytest.fixture
def tamu():
    return aplikasi.app.test_client()


@pytest.fixture
def pemilik(kirim):
    client = aplikasi.app.test_client()
    kirim(client, "/login", username="pemilik_edu", password=SANDI_PEMILIK)
    return client


@pytest.fixture
def kasir(kirim):
    client = aplikasi.app.test_client()
    kirim(client, "/login", username="kasir_edu", password=SANDI_KASIR)
    return client
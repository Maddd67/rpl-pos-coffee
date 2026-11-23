import logging
import os
import secrets
import sqlite3
from datetime import date
from functools import wraps

from flask import (
    Flask,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import models
import percobaan
import services

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

PRODUKSI = os.environ.get("APP_ENV") == "production"
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    if PRODUKSI:
        raise RuntimeError("SECRET_KEY wajib diatur pada lingkungan produksi.")
    # Nilai bawaan hanya untuk pengembangan lokal.
    app.secret_key = "dev-educoffee-ganti-di-produksi"

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=PRODUKSI,
)
models.init_db()


def csrf_token():
    """Hasilkan dan simpan token CSRF acak per sesi."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]


app.jinja_env.globals["csrf_token"] = csrf_token


@app.before_request
def muat_pengguna():
    """Muat data pengguna aktif dari sesi ke g.pengguna."""
    pengguna_id = session.get("pengguna_id")
    g.pengguna = models.ambil_pengguna(pengguna_id) if pengguna_id else None


@app.before_request
def periksa_csrf():
    """Tolak permintaan POST yang tidak memiliki token CSRF valid (400)."""
    if request.method == "POST":
        dikirim = request.form.get("csrf_token", "").encode("utf-8")
        asli = session.get("csrf_token", "").encode("utf-8")
        if not asli or not secrets.compare_digest(dikirim, asli):
            app.logger.warning("CSRF gagal path=%r ip=%s", request.path, request.remote_addr)
            abort(400)


@app.after_request
def tambah_header_keamanan(respons):
    respons.headers["X-Content-Type-Options"] = "nosniff"
    respons.headers["X-Frame-Options"] = "DENY"
    respons.headers["Referrer-Policy"] = "same-origin"
    return respons


def peran_diperlukan(*peran):
    """Batasi rute: belum login -> /login?next=...; peran tidak sesuai -> 403."""
    def dekorator(fungsi):
        @wraps(fungsi)
        def bungkus(*args, **kwargs):
            if g.pengguna is None:
                return redirect(url_for("login", next=request.full_path.rstrip("?")))
            if g.pengguna["peran"] not in peran:
                abort(403)
            return fungsi(*args, **kwargs)
        return bungkus
    return dekorator


semua_peran = peran_diperlukan(*services.PERAN)
hanya_pemilik = peran_diperlukan("pemilik")


def _tujuan_aman(tujuan):
    """Izinkan hanya path internal relatif agar tidak terjadi open redirect."""
    if tujuan and tujuan.startswith("/") and not tujuan.startswith("//") and "\\" not in tujuan:
        return tujuan
    return None


def _form_barang(judul, barang, galat, dengan_stok):
    """Render form tambah/ubah barang."""
    return render_template(
        "barang_form.html",
        judul=judul,
        barang=barang,
        galat=galat,
        dengan_stok=dengan_stok,
    )


@app.errorhandler(400)
def permintaan_buruk(_galat):
    return render_template("400.html"), 400


@app.errorhandler(403)
def akses_ditolak(_galat):
    pengguna = g.pengguna["username"] if g.get("pengguna") else "-"
    app.logger.warning("akses ditolak user=%r path=%r", pengguna, request.path)
    return render_template("403.html"), 403


@app.route("/login", methods=["GET", "POST"])
def login():
    galat, status = [], 200
    username_input = request.form.get("username", "")
    if request.method == "POST":
        bersih_user = username_input.strip()
        kunci = f"{request.remote_addr}|{bersih_user.lower()}"
        if percobaan.terkunci(kunci):
            app.logger.warning("login terkunci user=%r ip=%s", bersih_user, request.remote_addr)
            galat.append("Terlalu banyak percobaan gagal. Coba lagi beberapa menit lagi.")
            status = 429
        else:
            pengguna = services.autentikasi(bersih_user, request.form.get("password"))
            if pengguna:
                percobaan.reset(kunci)
                session.clear()
                session["pengguna_id"] = pengguna["id"]
                app.logger.info("login berhasil user=%r", pengguna["username"])
                tujuan_next = _tujuan_aman(request.form.get("next") or request.args.get("next"))
                return redirect(tujuan_next or url_for("daftar_barang"))
            percobaan.catat_gagal(kunci)
            app.logger.warning("login gagal user=%r ip=%s", bersih_user, request.remote_addr)
            galat.append("Nama pengguna atau kata sandi salah.")
            status = 401
    next_val = _tujuan_aman(request.args.get("next")) or ""
    return render_template("login.html", galat=galat, username=bersih_user if request.method == "POST" else "", next_url=next_val), status


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Anda telah keluar dari sistem Edu Coffee.")
    return redirect(url_for("login"))


@app.route("/")
@semua_peran
def beranda():
    return redirect(url_for("daftar_barang"))


@app.route("/barang")
@semua_peran
def daftar_barang():
    kata = request.args.get("q", "").strip()
    menipis = request.args.get("status") == "menipis"
    barang = models.cari_barang(kata, menipis)
    return render_template(
        "barang_list.html",
        barang=barang,
        kata=kata,
        menipis=menipis,
    )


@app.route("/barang/tambah", methods=["GET", "POST"])
@hanya_pemilik
def tambah_barang():
    if request.method == "POST":
        data, galat = services.validasi_barang(request.form)
        if not galat:
            try:
                models.tambah_barang(
                    data["nama"],
                    data["harga_jual"],
                    data["stok"],
                    data["stok_minimum"],
                )
            except sqlite3.IntegrityError:
                galat.append("Nama barang sudah ada.")
            else:
                flash("Barang berhasil ditambahkan.")
                return redirect(url_for("daftar_barang"))
        return _form_barang("Tambah Barang", request.form, galat, True)
    return _form_barang("Tambah Barang", {}, [], True)


@app.route("/barang/<int:barang_id>/ubah", methods=["GET", "POST"])
@hanya_pemilik
def ubah_barang(barang_id):
    barang = models.ambil_barang(barang_id)
    if barang is None:
        abort(404)
    if request.method == "POST":
        data, galat = services.validasi_barang(request.form, dengan_stok=False)
        if not galat:
            try:
                models.ubah_barang(
                    barang_id,
                    data["nama"],
                    data["harga_jual"],
                    data["stok_minimum"],
                )
            except sqlite3.IntegrityError:
                galat.append("Nama barang sudah ada.")
            else:
                flash("Barang berhasil diubah.")
                return redirect(url_for("daftar_barang"))
        return _form_barang("Ubah Barang", request.form, galat, False)
    return _form_barang("Ubah Barang", dict(barang), [], False)


@app.route("/barang/<int:barang_id>/hapus", methods=["POST"])
@hanya_pemilik
def hapus_barang(barang_id):
    if models.ambil_barang(barang_id) is None:
        abort(404)
    try:
        models.hapus_barang(barang_id)
    except sqlite3.IntegrityError:
        flash("Barang tidak dapat dihapus karena sudah dipakai pada transaksi.")
    else:
        flash("Barang berhasil dihapus.")
    return redirect(url_for("daftar_barang"))


@app.route("/masuk")
@hanya_pemilik
def daftar_masuk():
    return render_template("masuk_list.html", masuk=models.semua_barang_masuk())


@app.route("/masuk/tambah", methods=["GET", "POST"])
@hanya_pemilik
def tambah_masuk():
    galat, isian = [], {"tanggal": date.today().isoformat()}
    if request.method == "POST":
        isian = request.form
        data, galat = services.validasi_barang_masuk(request.form)
        if not galat and models.ambil_barang(data["barang_id"]) is None:
            galat.append("Barang tidak ditemukan.")
        if not galat:
            try:
                models.tambah_barang_masuk(
                    data["barang_id"],
                    data["jumlah"],
                    data["tanggal"],
                )
            except sqlite3.IntegrityError:
                galat.append("Barang tidak ditemukan.")
            else:
                flash("Barang masuk dicatat dan stok bertambah.")
                return redirect(url_for("daftar_masuk"))
    return render_template(
        "masuk_form.html",
        barang=models.cari_barang(),
        isian=isian,
        galat=galat,
    )


if __name__ == "__main__":
    # Mode debug hanya aktif bila FLASK_DEBUG=1 dan bukan di lingkungan produksi.
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1" and not PRODUKSI)
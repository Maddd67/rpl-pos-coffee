import os
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
import services

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-educoffee-ganti-di-produksi")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
models.init_db()


@app.before_request
def muat_pengguna():
    """Muat data pengguna aktif dari sesi ke g.pengguna."""
    pengguna_id = session.get("pengguna_id")
    g.pengguna = models.ambil_pengguna(pengguna_id) if pengguna_id else None


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


@app.errorhandler(403)
def akses_ditolak(_galat):
    return render_template("403.html"), 403


@app.route("/login", methods=["GET", "POST"])
def login():
    galat = []
    username_input = ""
    if request.method == "POST":
        username_input = (request.form.get("username") or "").strip()
        pengguna = services.autentikasi(username_input, request.form.get("password"))
        if pengguna:
            session.clear()
            session["pengguna_id"] = pengguna["id"]
            tujuan_next = _tujuan_aman(request.form.get("next") or request.args.get("next"))
            return redirect(tujuan_next or url_for("daftar_barang"))
        galat.append("Nama pengguna atau kata sandi salah.")
    next_val = _tujuan_aman(request.args.get("next")) or ""
    return render_template("login.html", galat=galat, username=username_input, next_url=next_val)


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
    app.run(debug=True)
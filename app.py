import os
import sqlite3
from datetime import date

from flask import Flask, abort, flash, redirect, render_template, request, url_for

import models
import services

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-educoffee-ganti-di-produksi")
models.init_db()


def _form_barang(judul, barang, galat, dengan_stok):
    """Render form tambah/ubah barang agar tidak duplikatif."""
    return render_template(
        "barang_form.html",
        judul=judul,
        barang=barang,
        galat=galat,
        dengan_stok=dengan_stok,
    )


@app.route("/")
def beranda():
    return redirect(url_for("daftar_barang"))


@app.route("/barang")
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
def daftar_masuk():
    return render_template("masuk_list.html", masuk=models.semua_barang_masuk())


@app.route("/masuk/tambah", methods=["GET", "POST"])
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
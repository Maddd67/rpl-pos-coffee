import os
import sqlite3
from flask import Flask, abort, flash, redirect, render_template, request, url_for
import models
import services

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-educoffee-ganti-di-produksi")
models.init_db()


@app.route("/")
def beranda():
    return redirect(url_for("daftar_barang"))


@app.route("/barang")
def daftar_barang():
    return render_template("barang_list.html", barang=models.semua_barang())


@app.route("/barang/tambah", methods=["GET", "POST"])
def tambah_barang():
    if request.method == "POST":
        data, galat = services.validasi_barang(request.form)
        if not galat:
            try:
                models.tambah_barang(data["nama"], data["harga_jual"], data["stok"], data["stok_minimum"])
            except sqlite3.IntegrityError:
                galat.append("Nama menu / bahan sudah terdaftar.")
            else:
                flash("Data berhasil ditambahkan ke katalog Edu Coffee.")
                return redirect(url_for("daftar_barang"))
        return render_template("barang_form.html", judul="Tambah Menu / Bahan", barang=request.form, galat=galat, dengan_stok=True)
    return render_template("barang_form.html", judul="Tambah Menu / Bahan", barang={}, galat=[], dengan_stok=True)


@app.route("/barang/<int:barang_id>/ubah", methods=["GET", "POST"])
def ubah_barang(barang_id):
    barang = models.ambil_barang(barang_id)
    if barang is None:
        abort(404)
    if request.method == "POST":
        data, galat = services.validasi_barang(request.form, dengan_stok=False)
        if not galat:
            try:
                models.ubah_barang(barang_id, data["nama"], data["harga_jual"], data["stok_minimum"])
            except sqlite3.IntegrityError:
                galat.append("Nama menu / bahan sudah terdaftar.")
            else:
                flash("Data berhasil diperbarui.")
                return redirect(url_for("daftar_barang"))
        return render_template("barang_form.html", judul="Ubah Menu / Bahan", barang=request.form, galat=galat, dengan_stok=False)
    return render_template("barang_form.html", judul="Ubah Menu / Bahan", barang=dict(barang), galat=[], dengan_stok=False)


@app.route("/barang/<int:barang_id>/hapus", methods=["POST"])
def hapus_barang(barang_id):
    if models.ambil_barang(barang_id) is None:
        abort(404)
    try:
        models.hapus_barang(barang_id)
    except sqlite3.IntegrityError:
        flash("Data tidak dapat dihapus karena sudah tercatat dalam transaksi.")
    else:
        flash("Data berhasil dihapus.")
    return redirect(url_for("daftar_barang"))


if __name__ == "__main__":
    app.run(debug=True)
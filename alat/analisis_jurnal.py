"""Rekap Jurnal Vibe Coding: python alat/analisis_jurnal.py jurnal/*.md"""
import re
import sys
from collections import Counter
from pathlib import Path

KEPUTUSAN = ("terima", "ubah", "tolak")


def baca_entri(berkas):
    """Baca baris tabel Markdown berkolom Keputusan dari berkas jurnal."""
    entri, kolom = [], None
    for baris in Path(berkas).read_text(encoding="utf-8").splitlines():
        if not baris.strip().startswith("|"):
            continue
        sel = [s.strip() for s in baris.strip().strip("|").split("|")]
        if all(set(s) <= set("-: ") for s in sel):
            continue
        if kolom is None:
            nama = [s.lower() for s in sel]
            if "keputusan" in nama:
                kolom = {n: i for i, n in enumerate(nama)}
            continue
        if len(sel) >= len(kolom):
            entri.append({n: sel[i] for n, i in kolom.items()})
    return entri


def rekap(entri):
    """Hitung keputusan, tag, dan jenis galat AI."""
    keputusan, tag, galat = Counter(), Counter(), Counter()
    for e in entri:
        k = e.get("keputusan", "").lower()
        keputusan[next((x for x in KEPUTUSAN if k.startswith(x)), "lain")] += 1
        gabungan = e.get("tujuan", "") + " " + e.get("alasan", "")
        for t in re.findall(r"\[([^\]]+)\]", gabungan):
            if t.lower().startswith("galat:"):
                galat[t.split(":", 1)[1].strip().lower()] += 1
            else:
                tag[t.lower()] += 1
    return keputusan, tag, galat


def persen(n, total):
    return f"{100 * n / total:.1f}%" if total else "-"


def cetak(judul, entri):
    total = len(entri)
    keputusan, tag, galat = rekap(entri)
    print(f"\n## {judul}  ({total} entri)")
    print("| Keputusan | Jumlah | Persen |\n|---|---|---|")
    for k in (*KEPUTUSAN, "lain"):
        if keputusan[k] or k != "lain":
            print(f"| {k.capitalize()} | {keputusan[k]} | {persen(keputusan[k], total)} |")
    if keputusan["lain"]:
        print(f"PERINGATAN: {keputusan['lain']} entri tanpa keputusan Terima/Ubah/Tolak -- rapikan jurnal.")
    if galat:
        print("\n| Jenis galat AI | Jumlah |\n|---|---|")
        for nama, n in galat.most_common():
            print(f"| {nama} | {n} |")
    if tag:
        print("\nTag: " + ", ".join(f"[{t}] {n}" for t, n in tag.most_common()))


if __name__ == "__main__":
    berkas = sys.argv[1:]
    if not berkas:
        sys.exit("Pemakaian: python alat/analisis_jurnal.py jurnal/*.md")
    semua = []
    for b in berkas:
        e = baca_entri(b)
        cetak(Path(b).stem, e)
        semua += e
    if len(berkas) > 1:
        cetak("GABUNGAN", semua)
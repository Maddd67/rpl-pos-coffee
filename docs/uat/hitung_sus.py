"""Hitung skor SUS (System Usability Scale) untuk responden UAT Edu Coffee."""

JAWABAN = {
    "Pemilik": [4, 2, 4, 1, 4, 2, 5, 2, 4, 1],
    "Kasir": [5, 1, 4, 2, 4, 1, 5, 1, 5, 2],
}


def skor_sus(jawaban):
    assert len(jawaban) == 10 and all(1 <= x <= 5 for x in jawaban), "Harus 10 jawaban (1-5)"
    total = sum((x - 1) if i % 2 == 0 else (5 - x) for i, x in enumerate(jawaban))
    return total * 2.5


if __name__ == "__main__":
    hasil = {nama: skor_sus(nilai) for nama, nilai in JAWABAN.items()}
    for nama, skor in hasil.items():
        print(f"{nama:10s}: {skor:5.1f}")
    rata_rata = sum(hasil.values()) / len(hasil)
    print(f"{'Rata-rata':10s}: {rata_rata:5.1f}")
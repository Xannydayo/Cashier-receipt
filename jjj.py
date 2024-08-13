import pandas as pd
from datetime import datetime
import pytz
from tabulate import tabulate
import os

# Set timezone to WIB (Western Indonesian Time)
indonesia_wib = pytz.timezone('Asia/Jakarta')
utc_now = datetime.utcnow()
wib_now = utc_now.replace(tzinfo=pytz.utc).astimezone(indonesia_wib)
formatted_wib_now = wib_now.strftime('%A, %d %B %Y %H:%M:%S %Z')
# Header for the receipt
header_struk = f"""
IJAN FOTOKOPI
JL. RADEN SALEH NO 45
KARANG TENGAH CILEDUG
NPWP : 01.780.859.3-013.000
DATE : {formatted_wib_now}
--------------------------------
"""

print(header_struk)

# Function to format currency to Rupiah
def formatrupiah(uang):
    y = str(uang)
    if len(y) <= 3:
        return "Rp " + y
    else:
        p = y[-3:]
        q = y[:-3]
        return formatrupiah(q) + "." + p

# Data Produk
produk = {
    "Kode": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
    "Barang": [
        "Hitam A4",
        "Warna A4",
        "Hitam F4",
        "Warna F4",
        "Spiral",
        "Lakban",
        "Binder Clip",
        "Stapler",
        "Kertas HVS",
        "Pulpen",
        "Pensil",
        "Penghapus",
        "Penggaris",
        "Map",
        "Amplop",
        "Stiker",
        "Kalkulator",
        "Gunting",
        "Lem",
        "Tipe-X",
    ],
    "Harga": [500, 1000, 600, 1200, 5000, 7000, 2000, 15000, 30000, 3000, 2000, 1000, 1500, 2500, 500, 1000, 50000, 10000, 3000, 2500],
}

# Konversi ke DataFrame
df_produk = pd.DataFrame(produk)

while True:  # Loop untuk mengulangi keseluruhan proses transaksi
    # Tampilkan Tabel Produk
    print("\nDaftar Produk:")
    print(tabulate(df_produk[["Kode", "Barang", "Harga"]], headers="keys", tablefmt="psql", showindex=False))

    # Input dari Pengguna
    pesanan = []

    while True:
        kode = input("Masukkan Kode Barang [A-T] atau 'ok' untuk mengakhiri: ").upper()
        if kode == 'OK':
            break
        if kode not in df_produk["Kode"].values:
            print("Kode barang tidak valid. Silakan coba lagi.")
            continue

        try:
            jumlah = int(input("Jumlah Barang: "))
            if jumlah <= 0:
                raise ValueError("Jumlah barang harus lebih dari 0")

            harga = int(input("Masukkan harga barang: "))
            if harga <= 0:
                raise ValueError("Harga barang harus lebih dari 0")

        except ValueError as e:
            print(f"Input tidak valid: {e}.")
            continue

        barang = df_produk[df_produk["Kode"] == kode].iloc[0]
        total = harga * jumlah
        pesanan.append([barang["Barang"], harga, jumlah, total])

    # Konversi Pesanan ke DataFrame
    df_pesanan = pd.DataFrame(
        pesanan, columns=["Nama Barang", "Harga", "Qty", "Total"]
    )
    # Calculate Total
    total_pembelian = df_pesanan["Total"].sum()

    # Display Receipt
    receipt_str = f"""{header_struk}
Nama Barang  Harga  Qty  Total
----------------------------
"""
    for index, row in df_pesanan.iterrows():
        nama_barang = row['Nama Barang'][:12]
        receipt_str += f"{nama_barang:<12} {row['Harga']:>5} {row['Qty']:>3} {row['Total']:>6}\n"

    receipt_str += f"""
----------------------------
Total : {formatrupiah(int(total_pembelian))}
"""

    print(receipt_str)
    print(f"Total: {formatrupiah(int(total_pembelian))}")

    # Pembayaran dan Kembalian
    while True:
        try:
            jumlah_bayar = int(input("Bayar : Rp "))
            if jumlah_bayar >= total_pembelian:
                kembalian = jumlah_bayar - total_pembelian
                rincian_pembayaran = f"""
Bayar : {formatrupiah(int(jumlah_bayar))}
Kembali: {formatrupiah(int(kembalian))}
"""
                receipt_str += rincian_pembayaran
                break
            else:
                print("Uang tidak cukup.")
        except ValueError:
            print("Masukkan angka valid.")

    # Footer for the receipt
    footer_struk = """
----------------------------
      TERIMA KASIH          
----------------------------
"""
    receipt_str += footer_struk
    print(receipt_str)

    # Save receipt to file and print
    with open("receipt.txt", "w") as f:
        f.write(receipt_str)

    # Print receipt using notepad (Windows)
    os.system("notepad receipt.txt")

    # Tanya pengguna apakah ingin melakukan transaksi lain
    ulangi = input("\nApakah Anda ingin melakukan transaksi lain? (y/t): ").lower()
    if ulangi != "y":
        break

    print('')
import tkinter as tk
from tkinter import messagebox

# Data awal
menu = {
    1: {"nama": "Nasi Goreng", "harga": 20000, "stok": 10},
    2: {"nama": "Mie Goreng", "harga": 18000, "stok": 8},
    3: {"nama": "Ayam Bakar", "harga": 25000, "stok": 5},
    4: {"nama": "Sate Ayam", "harga": 22000, "stok": 7},
}

keranjang = {}
saldo_pengguna = 100000  # Saldo awal pengguna
riwayat_pemesanan = []

# Fungsi untuk menampilkan menu makanan
def tampilkan_menu():
    menu_str = "=== Daftar Menu ===\n"
    for id_menu, item in menu.items():
        menu_str += f"{id_menu}. {item['nama']} - Rp{item['harga']} (Stok: {item['stok']})\n"
    messagebox.showinfo("Menu", menu_str)

# Fungsi untuk menambah makanan ke keranjang
def tambah_ke_keranjang():
    def proses_tambah():
        try:
            id_menu = int(entry_id.get())
            jumlah = int(entry_jumlah.get())
            if id_menu in menu and jumlah <= menu[id_menu]["stok"]:
                if id_menu in keranjang:
                    keranjang[id_menu] += jumlah
                else:
                    keranjang[id_menu] = jumlah
                messagebox.showinfo("Sukses", "Item berhasil ditambahkan ke keranjang.")
                tambah_window.destroy()
            else:
                messagebox.showerror("Error", "Stok tidak mencukupi atau ID menu tidak ditemukan.")
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid.")
    
    tambah_window = tk.Toplevel(root)
    tambah_window.title("Tambah ke Keranjang")
    tambah_window.config(bg="#FFEB3B")
    
    tk.Label(tambah_window, text="ID Menu:", font=("Arial", 12), bg="#FFEB3B").grid(row=0, column=0, padx=10, pady=10)
    entry_id = tk.Entry(tambah_window, font=("Arial", 12))
    entry_id.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(tambah_window, text="Jumlah:", font=("Arial", 12), bg="#FFEB3B").grid(row=1, column=0, padx=10, pady=10)
    entry_jumlah = tk.Entry(tambah_window, font=("Arial", 12))
    entry_jumlah.grid(row=1, column=1, padx=10, pady=10)
    
    tk.Button(tambah_window, text="Tambah", command=proses_tambah, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

# Fungsi untuk menampilkan isi keranjang
def tampilkan_keranjang():
    if keranjang:
        keranjang_str = "=== Keranjang Belanja ===\n"
        total = 0
        for id_menu, jumlah in keranjang.items():
            item = menu[id_menu]
            subtotal = item["harga"] * jumlah
            keranjang_str += f"{item['nama']} x{jumlah} - Rp{subtotal}\n"
            total += subtotal
        keranjang_str += f"Total: Rp{total}"
        messagebox.showinfo("Keranjang", keranjang_str)
    else:
        messagebox.showinfo("Keranjang", "Keranjang kosong.")

# Fungsi untuk melakukan checkout
def checkout():
    global saldo_pengguna
    if keranjang:
        total = sum(menu[id_menu]["harga"] * jumlah for id_menu, jumlah in keranjang.items())
        diskon = total * 0.1  # 10% diskon
        total_diskon = total - diskon
        
        if saldo_pengguna >= total_diskon:
            for id_menu, jumlah in keranjang.items():
                menu[id_menu]["stok"] -= jumlah
            riwayat_pemesanan.append({"keranjang": keranjang.copy(), "total": total_diskon})
            saldo_pengguna -= total_diskon
            keranjang.clear()
            messagebox.showinfo("Sukses", f"Pembayaran berhasil. Total: Rp{total_diskon}\nSisa saldo: Rp{saldo_pengguna}")
        else:
            messagebox.showerror("Error", "Saldo tidak mencukupi.")
    else:
        messagebox.showinfo("Checkout", "Keranjang kosong.")

# Fungsi untuk menampilkan riwayat pemesanan
def tampilkan_riwayat():
    if riwayat_pemesanan:
        riwayat_str = "=== Riwayat Pemesanan ===\n"
        for i, riwayat in enumerate(riwayat_pemesanan, 1):
            riwayat_str += f"Pesanan {i}:\n"
            for id_menu, jumlah in riwayat["keranjang"].items():
                item = menu[id_menu]
                riwayat_str += f"  {item['nama']} x{jumlah}\n"
            riwayat_str += f"  Total: Rp{riwayat['total']}\n"
        messagebox.showinfo("Riwayat", riwayat_str)
    else:
        messagebox.showinfo("Riwayat", "Belum ada riwayat pemesanan.")

# Setup GUI utama
root = tk.Tk()
root.title("YuFood - Aplikasi Pemesanan Makanan")
root.geometry("500x600")
root.config(bg="#FFEB3B")

# Header dengan nama toko
header_label = tk.Label(root, text="YuFood", font=("Arial", 24, "bold"), bg="#FFEB3B", fg="#4CAF50")
header_label.pack(pady=20)

# Tombol-tombol utama
tk.Button(root, text="Tampilkan Menu", command=tampilkan_menu, font=("Arial", 12), bg="#4CAF50", fg="white", width=30).pack(pady=5)
tk.Button(root, text="Tambah ke Keranjang", command=tambah_ke_keranjang, font=("Arial", 12), bg="#FF9800", fg="white", width=30).pack(pady=5)
tk.Button(root, text="Tampilkan Keranjang", command=tampilkan_keranjang, font=("Arial", 12), bg="#2196F3", fg="white", width=30).pack(pady=5)
tk.Button(root, text="Checkout", command=checkout, font=("Arial", 12), bg="#4CAF50", fg="white", width=30).pack(pady=5)
tk.Button(root, text="Tampilkan Riwayat", command=tampilkan_riwayat, font=("Arial", 12), bg="#9C27B0", fg="white", width=30).pack(pady=5)
tk.Button(root, text="Keluar", command=root.quit, font=("Arial", 12), bg="#f44336", fg="white", width=30).pack(pady=5)

root.mainloop()

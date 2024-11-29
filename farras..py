import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

conn = sqlite3.connect('kpop_store.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS merchandise (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    kategori TEXT NOT NULL,
    harga INTEGER NOT NULL,
    stok INTEGER NOT NULL
)
""")
conn.commit()

def tambah_data():
    nama = entry_nama.get()
    kategori = entry_kategori.get()
    harga = entry_harga.get()
    stok = entry_stok.get()
    
    if nama and kategori and harga and stok:
        cursor.execute("INSERT INTO merchandise (nama, kategori, harga, stok) VALUES (?, ?, ?, ?)",
                       (nama, kategori, int(harga), int(stok)))
        conn.commit()
        tampilkan_data()
        messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
        reset_form()
    else:
        messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")

def tampilkan_data():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM merchandise")
    for data in cursor.fetchall():
        tree.insert("", "end", values=data)

def hapus_data():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        id_data = item['values'][0]
        cursor.execute("DELETE FROM merchandise WHERE id = ?", (id_data,))
        conn.commit()
        tampilkan_data()
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
    else:
        messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus!")

def tambah_ke_keranjang():
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        data = item['values']
        keranjang_tree.insert("", "end", values=(data[1], data[3], 1, data[3]))  # Nama, Harga, Jumlah, Subtotal
        update_total()
    else:
        messagebox.showwarning("Peringatan", "Pilih data yang akan ditambahkan ke keranjang!")

def hapus_dari_keranjang():
    selected_item = keranjang_tree.selection()
    if selected_item:
        keranjang_tree.delete(selected_item)
        update_total()
    else:
        messagebox.showwarning("Peringatan", "Pilih item di keranjang yang akan dihapus!")
 
def checkout():
    if keranjang_tree.get_children():
        keranjang_tree.delete(*keranjang_tree.get_children())
        update_total()
        messagebox.showinfo("Sukses", "Transaksi berhasil! Keranjang telah dikosongkan.")
    else:
        messagebox.showwarning("Peringatan", "Keranjang masih kosong!")

def update_total():
    total = 0
    for item in keranjang_tree.get_children():
        subtotal = keranjang_tree.item(item)['values'][3]  # Subtotal ada di kolom ke-4
        total += subtotal
    total_var.set(f"Total: IDR {total}")

def reset_form():
    entry_nama.delete(0, END)
    entry_kategori.delete(0, END)
    entry_harga.delete(0, END)
    entry_stok.delete(0, END)

root = Tk()
root.title("K-Pop Store Management")
root.geometry("900x700")
root.configure(bg="#DCEEFF")

header = Frame(root, bg="#0052CC", pady=10)
header.pack(fill=X)
Label(header, text="K-Pop Store Management", bg="#0052CC", fg="white", font=("Arial", 16, "bold")).pack()

frame_form = Frame(root, bg="#DCEEFF", padx=10, pady=10)
frame_form.pack()

Label(frame_form, text="Nama Merchandise", bg="#DCEEFF", font=("Arial", 10)).grid(row=0, column=0, sticky=W, pady=5)
Label(frame_form, text="Kategori", bg="#DCEEFF", font=("Arial", 10)).grid(row=1, column=0, sticky=W, pady=5)
Label(frame_form, text="Harga", bg="#DCEEFF", font=("Arial", 10)).grid(row=2, column=0, sticky=W, pady=5)
Label(frame_form, text="Stok", bg="#DCEEFF", font=("Arial", 10)).grid(row=3, column=0, sticky=W, pady=5)

entry_nama = Entry(frame_form, width=30)
entry_kategori = Entry(frame_form, width=30)
entry_harga = Entry(frame_form, width=30)
entry_stok = Entry(frame_form, width=30)

entry_nama.grid(row=0, column=1, pady=5)
entry_kategori.grid(row=1, column=1, pady=5)
entry_harga.grid(row=2, column=1, pady=5)
entry_stok.grid(row=3, column=1, pady=5)

Button(frame_form, text="Tambah Data", command=tambah_data, bg="#007BFF", fg="white", width=15).grid(row=4, column=0, pady=10)
Button(frame_form, text="Reset Form", command=reset_form, bg="#F44336", fg="white", width=15).grid(row=4, column=1, pady=10)

frame_table = Frame(root, bg="#DCEEFF", padx=10, pady=10)
frame_table.pack()

tree = ttk.Treeview(frame_table, columns=("ID", "Nama", "Kategori", "Harga", "Stok"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nama", text="Nama Merchandise")
tree.heading("Kategori", text="Kategori")
tree.heading("Harga", text="Harga")
tree.heading("Stok", text="Stok")
tree.column("ID", width=50, anchor=CENTER)
tree.column("Nama", width=200)
tree.column("Kategori", width=150)
tree.column("Harga", width=100, anchor=CENTER)
tree.column("Stok", width=100, anchor=CENTER)
tree.pack(fill=BOTH, expand=True)

Button(frame_table, text="Tambah ke Keranjang", command=tambah_ke_keranjang, bg="#4CAF50", fg="white", width=20).pack(pady=5)


frame_keranjang = Frame(root, bg="#DCEEFF", padx=10, pady=10)
frame_keranjang.pack()

Label(frame_keranjang, text="Keranjang Belanja", bg="#DCEEFF", font=("Arial", 12, "bold")).pack()

keranjang_tree = ttk.Treeview(frame_keranjang, columns=("Nama", "Harga", "Jumlah", "Subtotal"), show="headings")
keranjang_tree.heading("Nama", text="Nama Merchandise")
keranjang_tree.heading("Harga", text="Harga")
keranjang_tree.heading("Jumlah", text="Jumlah")
keranjang_tree.heading("Subtotal", text="Subtotal")
keranjang_tree.column("Nama", width=200)
keranjang_tree.column("Harga", width=100, anchor=CENTER)
keranjang_tree.column("Jumlah", width=100, anchor=CENTER)
keranjang_tree.column("Subtotal", width=100, anchor=CENTER)
keranjang_tree.pack(fill=BOTH, expand=True)

Button(frame_keranjang, text="Hapus dari Keranjang", command=hapus_dari_keranjang, bg="#F44336", fg="white", width=20).pack(pady=5)

total_var = StringVar()
total_var.set("Total: IDR 0")

Label(frame_keranjang, textvariable=total_var, bg="#DCEEFF", font=("Arial", 12, "bold")).pack()
Button(frame_keranjang, text="Checkout", command=checkout, bg="#007BFF", fg="white", width=20).pack(pady=10)

tampilkan_data()

root.mainloop()

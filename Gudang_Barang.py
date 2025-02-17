import streamlit as st
import pandas as pd
import os
from abc import ABC, abstractmethod
import hydralit_components as hc
import matplotlib.pyplot as plt

# Kelas Abstrak BarangBase
class BarangBase(ABC):
    def __init__(self, id, nama, harga, stok):
        self.id = id
        self.nama = nama
        self.harga = harga
        self.stok = stok
    
    @abstractmethod
    def info_barang(self):
        pass

# Kelas Elektronik
class Elektronik(BarangBase):
    def __init__(self, id, nama, harga, stok, merek, garansi):
        super().__init__(id, nama, harga, stok)
        self.merek = merek
        self.garansi = garansi
    
    def info_barang(self):
        info = f"ID: {self.id}, Nama: {self.nama}, Harga: {self.harga:,} IDR, Stok: {self.stok}"
        return f"{info}, Merek: {self.merek}, Garansi: {self.garansi} tahun"

# Kelas Pakaian
class Pakaian(BarangBase):
    def __init__(self, id, nama, harga, stok, ukuran, bahan):
        super().__init__(id, nama, harga, stok)
        self.ukuran = ukuran
        self.bahan = bahan
    
    def info_barang(self):
        info = f"ID: {self.id}, Nama: {self.nama}, Harga: {self.harga:,} IDR, Stok: {self.stok}"
        return f"{info}, Ukuran: {self.ukuran}, Bahan: {self.bahan}"

# Kelas Gudang
class Gudang:
    def __init__(self):
        self.daftar_barang = []
    
    def tambah_barang(self, barang):
        self.daftar_barang.append(barang)
    
    def cari_barang(self, id):
        for barang in self.daftar_barang:
            if barang.id == id:
                return barang
        return None
    
    def tampilkan_semua_barang(self):
        return [barang.info_barang() for barang in self.daftar_barang]
    
    def update_stok(self, id, jumlah):
        barang = self.cari_barang(id)
        if barang:
            barang.stok += jumlah
            return f"Stok barang {barang.nama} berhasil diperbarui."
        else:
            return f"Barang dengan ID {id} tidak ditemukan di gudang."
    
    def hapus_barang(self, id):
        barang = self.cari_barang(id)
        if barang:
            self.daftar_barang.remove(barang)
            return f"Barang dengan ID {id} berhasil dihapus."
        else:
            return f"Barang dengan ID {id} tidak ditemukan di gudang."
    
    def edit_barang(self, id, nama=None, harga=None, stok=None):
        barang = self.cari_barang(id)
        if barang:
            if nama:
                barang.nama = nama
            if harga:
                barang.harga = harga
            if stok:
                barang.stok = stok
            return f"Barang dengan ID {id} berhasil diperbarui."
        else:
            return f"Barang dengan ID {id} tidak ditemukan di gudang."
    
    def data_stok_barang(self):
        data = {"Nama": [], "Stok": []}
        for barang in self.daftar_barang:
            data["Nama"].append(barang.nama)
            data["Stok"].append(barang.stok)
        return pd.DataFrame(data)

def save_to_excel(gudang, filename="gudang_data.xlsx"):
    data = []
    for barang in gudang.daftar_barang:
        if isinstance(barang, Elektronik):
            jenis = "Elektronik"
            extra_info = {"Merek": barang.merek, "Garansi": barang.garansi}
        elif isinstance(barang, Pakaian):
            jenis = "Pakaian"
            extra_info = {"Ukuran": barang.ukuran, "Bahan": barang.bahan}
        
        data.append({
            "ID": barang.id,
            "Nama": barang.nama,
            "Harga": barang.harga,
            "Stok": barang.stok,
            "Jenis": jenis,
            **extra_info
        })
    
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def load_from_excel(filename="gudang_data.xlsx"):
    if os.path.exists(filename):
        df = pd.read_excel(filename)
        for index, row in df.iterrows():
            if row["Jenis"] == "Elektronik":
                barang = Elektronik(row["ID"], row["Nama"], row["Harga"], row["Stok"], row["Merek"], row["Garansi"])
            elif row["Jenis"] == "Pakaian":
                barang = Pakaian(row["ID"], row["Nama"], row["Harga"], row["Stok"], row["Ukuran"], row["Bahan"])
            gudang.tambah_barang(barang)

# Inisialisasi Gudang
gudang = Gudang()
load_from_excel()

# Streamlit App
st.set_page_config(page_title="Sistem Inventarisasi Barang", layout="wide")


# Tambahkan CSS untuk styling
st.markdown(
    """
    <style>
    /* General Styles */
    .stButton>button {
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        border: none !important;
        transition: background-color 0.3s ease;
        font-weight: bold;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button:hover {
        background-color: #45a049 !important;
    }
    .stButton>button:focus {
        background-color: #3e8e41 !important;
    }

    /* Heading */
    .stMarkdown h1 {
        color: #4CAF50 !important;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* Subheading */
    .stMarkdown h2 {
        color: #45a049 !important;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        margin-top: 20px;
    }

    /* Selectbox and Input Fields */
    .stSelectbox, .stTextInput, .stNumberInput {
        background-color: #e8f5e9 !important;
        color: #1b5e20 !important;
        border: 1px solid #4CAF50 !important;
        border-radius: 8px !important;
        padding: 10px !important;
        margin-bottom: 20px;
        transition: background-color 0.3s ease;
    }
    .stSelectbox:hover, .stTextInput:hover, .stNumberInput:hover {
        background-color: #d0f0c0 !important;
    }

    /* Table */
    .stDataFrame {
        border: 2px solid #4CAF50 !important;
        border-radius: 8px !important;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    /* Custom Tooltip */
    .stMarkdown span:hover::after {
        content: attr(title);
        position: absolute;
        background-color: #4CAF50;
        color: white;
        padding: 5px;
        border-radius: 5px;
        top: 20px;
        left: 20px;
        white-space: nowrap;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# specify the primary menu definition
menu_data = [
    {'icon': "far fa-copy", 'label':"Tambah Barang"},
    {'icon': "far fa-chart-bar", 'label':"Lihat Barang"},
    {'icon': "far fa-address-book", 'label':"Cari Barang"},
    {'icon': "far fa-clone", 'label':"Update Stok"},
    {'icon': "fas fa-tachometer-alt", 'label':"Hapus Barang"},
    {'icon': "far fa-copy", 'label':"Edit Barang"},
]

# we can override any part of the primary colors of the menu
over_theme =	{'txc_inactive': '#FFFFFF','menu_background':'#4CAF50','txc_active':'#000000','option_active':'#FFFFFF'}

# Create sidebar with navigation
with st.sidebar:
    menu_id = hc.nav_bar(menu_definition=menu_data,	home_name='Home', override_theme=over_theme)

    
if menu_id == "Home":
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://dharmawacana.ac.id/home/wp-content/uploads/2021/06/LOGO-STMIK-DW-2021-294x300.png" alt="Logo Anda" width="400">
            <h3 style="font-size: 3em; margin-top: 20px;">Selamat Datang di Aplikasi Inventarisasi Barang</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

# Tambah Barang
if menu_id == "Tambah Barang":
    st.subheader("Tambah Barang")
    jenis = st.selectbox("Jenis Barang", ["Elektronik", "Pakaian"])
    id = st.number_input("ID", min_value=1)
    nama = st.text_input("Nama Barang")
    harga = st.number_input("Harga", min_value=0)
    stok = st.number_input("Stok", min_value=0)
    
    if jenis == "Elektronik":
        merek = st.text_input("Merek")
        garansi = st.number_input("Garansi (tahun)", min_value=0)
        if st.button("Tambah"):
            elektronik = Elektronik(id, nama, harga, stok, merek, garansi)
            gudang.tambah_barang(elektronik)
            save_to_excel(gudang)
            st.success(f"Barang elektronik '{nama}' berhasil ditambahkan!")
    
    elif jenis == "Pakaian":
        ukuran = st.text_input("Ukuran")
        bahan = st.text_input("Bahan")
        if st.button("Tambah"):
            pakaian = Pakaian(id, nama, harga, stok, ukuran, bahan)
            gudang.tambah_barang(pakaian)
            save_to_excel(gudang)
            st.success(f"Barang pakaian '{nama}' berhasil ditambahkan!")

# Lihat Barang
elif menu_id == "Lihat Barang":
    st.subheader("Daftar Barang di Gudang")
    daftar_barang = gudang.tampilkan_semua_barang()
    
    df_data = []
    for barang in gudang.daftar_barang:
        data = {
            "ID": barang.id,
            "Nama": barang.nama,
            "Harga": barang.harga,
            "Stok": barang.stok,
            "Jenis": barang.__class__.__name__,
        }
        if isinstance(barang, Elektronik):
            data["Merek"] = barang.merek
            data["Garansi/Tahun"] = barang.garansi
        elif isinstance(barang, Pakaian):
            data["Ukuran"] = barang.ukuran
            data["Bahan"] = barang.bahan
        df_data.append(data)
    
    df = pd.DataFrame(df_data)
    st.dataframe(df)
    
    # Grafik Stok Barang
    st.subheader("Grafik Stok Barang")
    data_stok = gudang.data_stok_barang()
    st.bar_chart(data_stok.set_index("Nama"))

# Cari Barang
elif menu_id == "Cari Barang":
    st.subheader("Cari Barang")
    id = st.number_input("Masukkan ID Barang", min_value=1)
    if st.button("Cari"):
        barang = gudang.cari_barang(id)
        if barang:
            data = {
                "ID": [barang.id],
                "Nama": [barang.nama],
                "Harga": [barang.harga],
                "Stok": [barang.stok],
                "Jenis": [barang.__class__.__name__]
            }
            if isinstance(barang, Elektronik):
                data["Merek"] = [barang.merek]
                data["Garansi/Tahun"] = [barang.garansi]
            elif isinstance(barang, Pakaian):
                data["Ukuran"] = [barang.ukuran]
                data["Bahan"] = [barang.bahan]
            
            df = pd.DataFrame(data)
            st.table(df)
        else:
            st.error(f"Barang dengan ID {id} tidak ditemukan.")

# Update Stok
elif menu_id == "Update Stok":
    st.subheader("Update Stok Barang")
    id = st.number_input("Masukkan ID Barang", min_value=1)
    jumlah = st.number_input("Jumlah Penambahan Stok", min_value=0)
    if st.button("Update"):
        pesan = gudang.update_stok(id, jumlah)
        save_to_excel(gudang)
        st.success(pesan)
        
        barang = gudang.cari_barang(id)
        if barang:
            data = {
                "ID": [barang.id],
                "Nama": [barang.nama],
                "Harga": [barang.harga],
                "Stok": [barang.stok],
                "Jenis": [barang.__class__.__name__]
            }
            if isinstance(barang, Elektronik):
                data["Merek"] = [barang.merek]
                data["Garansi/Tahun"] = [barang.garansi]
            elif isinstance(barang, Pakaian):
                data["Ukuran"] = [barang.ukuran]
                data["Bahan"] = [barang.bahan]
            
            df = pd.DataFrame(data)
            st.table(df)

# Hapus Barang
elif menu_id == "Hapus Barang":
    st.subheader("Hapus Barang")
    id = st.number_input("Masukkan ID Barang", min_value=1)
    if st.button("Hapus"):
        pesan = gudang.hapus_barang(id)
        save_to_excel(gudang)
        st.success(pesan)

# Edit Barang
elif menu_id == "Edit Barang":
    st.subheader("Edit Barang")
    id = st.number_input("Masukkan ID Barang", min_value=1)
    nama = st.text_input("Nama Barang (Kosongkan jika tidak ingin mengubah)")
    harga = st.number_input("Harga Barang (Kosongkan jika tidak ingin mengubah)", min_value=0, value=0)
    stok = st.number_input("Stok Barang (Kosongkan jika tidak ingin mengubah)", min_value=0, value=0)
    if st.button("Edit"):
        pesan = gudang.edit_barang(id, nama if nama else None, harga if harga > 0 else None, stok if stok > 0 else None)
        save_to_excel(gudang)
        st.success(pesan)
        
        barang = gudang.cari_barang(id)
        if barang:
            data = {
                "ID": [barang.id],
                "Nama": [barang.nama],
                "Harga": [barang.harga],
                "Stok": [barang.stok],
                "Jenis": [barang.__class__.__name__]
            }
            if isinstance(barang, Elektronik):
                data["Merek"] = [barang.merek]
                data["Garansi"] = [barang.garansi]
            elif isinstance(barang, Pakaian):
                data["Ukuran"] = [barang.ukuran]
                data["Bahan"] = [barang.bahan]
            
            df = pd.DataFrame(data)
            st.table(df)

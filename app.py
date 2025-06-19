import streamlit as st
import pandas as pd
import os
from utils import generate_keuangan_pdf

# Path file CSV
DATA_DIR = "data"
PROYEK_CSV = os.path.join(DATA_DIR, "proyek.csv")
KARYAWAN_CSV = os.path.join(DATA_DIR, "karyawan.csv")
KEUANGAN_CSV = os.path.join(DATA_DIR, "keuangan.csv")

# Load dan Simpan data
def load_data(path):
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()

def save_data(df, path):
    df.to_csv(path, index=False)

def halaman_proyek():
    st.title("📁 Data Proyek")
    df = load_data(PROYEK_CSV)

    st.subheader("Tambah Proyek Baru")
    with st.form("form_proyek"):
        nama = st.text_input("Nama Proyek")
        klien = st.text_input("Klien")
        tanggal_mulai = st.date_input("Tanggal Mulai")
        deadline = st.date_input("Deadline")
        status = st.selectbox("Status", ["Berjalan", "Selesai", "Dibatalkan"])
        keterangan = st.text_area("Keterangan")
        simpan = st.form_submit_button("Simpan")
        if simpan:
            new_row = {
                "id": len(df)+1,
                "nama": nama,
                "klien": klien,
                "tanggal_mulai": tanggal_mulai,
                "deadline": deadline,
                "status": status,
                "keterangan": keterangan
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df, PROYEK_CSV)
            st.success("✅ Proyek berhasil ditambahkan!")

    st.subheader("Daftar Proyek")

    if not df.empty:
        df["index"] = df.index
        selected_index = st.selectbox("Pilih Proyek untuk Edit/Hapus", df["index"])
        selected_row = df[df["index"] == selected_index].iloc[0]

        with st.expander("✏️ Edit Proyek"):
            with st.form("edit_proyek"):
                new_nama = st.text_input("Nama Proyek", selected_row["nama_proyek"])
                new_klien = st.text_input("Klien", selected_row["klien"])
                new_mulai = st.date_input("Tanggal Mulai", pd.to_datetime(selected_row["tanggal_mulai"]))
                new_deadline = st.date_input("Deadline", pd.to_datetime(selected_row["deadline"]))
                new_status = st.selectbox("Status", ["Berjalan", "Selesai", "Dibatalkan"], index=["Berjalan", "Selesai", "Dibatalkan"].index(selected_row["status"]))
                new_keterangan = st.text_area("Keterangan", selected_row["keterangan"])
                update = st.form_submit_button("Update")
                if update:
                    df.loc[selected_index, ["nama", "klien", "tanggal_mulai", "deadline", "status", "keterangan"]] = [
                        new_nama, new_klien, new_mulai, new_deadline, new_status, new_keterangan
                    ]
                    save_data(df, PROYEK_CSV)
                    st.success("✅ Proyek berhasil diperbarui!")

        if st.button("🗑️ Hapus Proyek Ini"):
            df = df.drop(index=selected_index).reset_index(drop=True)
            save_data(df, PROYEK_CSV)
            st.success("✅ Proyek berhasil dihapus!")

    st.dataframe(df)

def halaman_karyawan():
    st.title("👨‍💼 Data Karyawan")
    df = load_data(KARYAWAN_CSV)

    st.subheader("Tambah Karyawan Baru")
    with st.form("form_karyawan"):
        nama = st.text_input("Nama")
        posisi = st.text_input("Posisi")
        gaji = st.text_input("Gaji")
        email = st.text_input("Email")
        status = st.selectbox("Status", ["Aktif", "NonAktif"])
        simpan = st.form_submit_button("Simpan")
        if simpan:
            new_row = {
                "id": len(df) + 1,
                "nama": nama,
                "posisi": posisi,
                'gaji' : gaji,
                "email": email,
                "status": status
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df, KARYAWAN_CSV)
            st.success("✅ Karyawan berhasil ditambahkan!")

    st.subheader("Daftar Karyawan")

    if not df.empty:
        df["index"] = df.index
        selected_index = st.selectbox("Pilih baris untuk Edit/Hapus", df["index"])
        selected_row = df[df["index"] == selected_index].iloc[0]

        with st.expander("✏️ Edit Data Karyawan"):
            with st.form("edit_karyawan"):
                new_nama = st.text_input("Nama", selected_row["nama"])
                new_posisi = st.text_input("Posisi", selected_row["posisi"])
                new_gaji = st.text_input("Gaji", selected_row["gaji"])
                new_email = st.text_input("Email", selected_row["email"])
                new_status = st.selectbox("Status", ["Aktif", "NonAktif"], index=["Aktif", "NonAktif"].index(selected_row["status"]))
                update = st.form_submit_button("Update")
                if update:
                    df.loc[selected_index, ["nama", "posisi", "gaji", "email", "status"]] = [
                        new_nama, new_posisi, new_email, new_gaji, new_status
                    ]
                    save_data(df, KARYAWAN_CSV)
                    st.success("✅ Data karyawan berhasil diperbarui!")

        if st.button("🗑️ Hapus Karyawan Ini"):
            df = df.drop(index=selected_index).reset_index(drop=True)
            save_data(df, KARYAWAN_CSV)
            st.success("✅ Data karyawan berhasil dihapus!")

    st.dataframe(df)

    if st.button("📄 Cetak PDF Laporan Karyawan"):
        pdf_path = generate_karyawan_pdf()
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download PDF", f, file_name="laporan_karyawan.pdf")


# Halaman Keuangan
def halaman_keuangan():
    st.title("💰 Data Keuangan")
    df = load_data(KEUANGAN_CSV)

    st.subheader("Tambah Transaksi Baru")
    with st.form("form_keuangan"):
        tanggal = st.date_input("Tanggal")
        jenis = st.selectbox("Jenis", ["Pemasukan", "Pengeluaran"])
        kategori = st.text_input("Kategori")
        jumlah = st.number_input("Jumlah", min_value=0)
        keterangan = st.text_input("Keterangan")
        simpan = st.form_submit_button("Simpan")
        if simpan:
            new_row = {
                "id": len(df)+1,
                "tanggal": tanggal,
                "jenis": jenis,
                "kategori": kategori,
                "jumlah": jumlah,
                "keterangan": keterangan
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df, KEUANGAN_CSV)
            st.success("✅ Data keuangan disimpan!")

    st.subheader("Riwayat Keuangan")

    if not df.empty:
        df["index"] = df.index
        selected_index = st.selectbox("Pilih Baris untuk Edit/Hapus", df["index"])
        selected_row = df[df["index"] == selected_index].iloc[0]

        with st.expander("✏️ Edit Data"):
            with st.form("edit_form"):
                new_tanggal = st.date_input("Tanggal", pd.to_datetime(selected_row["tanggal"]))
                new_jenis = st.selectbox("Jenis", ["Pemasukan", "Pengeluaran"], index=["Pemasukan", "Pengeluaran"].index(selected_row["jenis"]))
                new_kategori = st.text_input("Kategori", selected_row["kategori"])
                new_jumlah = st.number_input("Jumlah", value=int(selected_row["jumlah"]), min_value=0)
                new_keterangan = st.text_input("Keterangan", selected_row["keterangan"])
                update = st.form_submit_button("Update")
                if update:
                    df.loc[selected_index, ["tanggal", "jenis", "kategori", "jumlah", "keterangan"]] = [
                        new_tanggal, new_jenis, new_kategori, new_jumlah, new_keterangan
                    ]
                    save_data(df, KEUANGAN_CSV)
                    st.success("✅ Data berhasil diperbarui!")

        if st.button("🗑️ Hapus Data Ini"):
            df = df.drop(index=selected_index).reset_index(drop=True)
            save_data(df, KEUANGAN_CSV)
            st.success("✅ Data berhasil dihapus!")

    st.dataframe(df)

    if st.button("📄 Cetak Laporan Keuangan ke PDF"):
        pdf_path = generate_keuangan_pdf()
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download PDF", f, file_name="laporan_keuangan.pdf")
        else:
            st.warning("⚠️ Gagal mencetak laporan. Data kosong atau error.")

# Sidebar Navigasi
st.sidebar.title("ERP Mini Perusahaan")
halaman = st.sidebar.radio("Pilih Menu", ["📁 Proyek", "👨‍💼 Karyawan", "💰 Keuangan"])

if halaman == "📁 Proyek":
    halaman_proyek()
elif halaman == "👨‍💼 Karyawan":
    halaman_karyawan()
elif halaman == "💰 Keuangan":
    halaman_keuangan()

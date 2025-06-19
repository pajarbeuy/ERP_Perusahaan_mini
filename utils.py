from fpdf import FPDF
import pandas as pd
import os

DATA_DIR = "data"
PROYEK_CSV = os.path.join(DATA_DIR, "proyek.csv")
KARYAWAN_CSV = os.path.join(DATA_DIR, "karyawan.csv")
KEUANGAN_CSV = os.path.join(DATA_DIR, "keuangan.csv")

# Fungsi umum ekspor PDF
def export_to_pdf(title, df, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=title, ln=True, align="C")
    pdf.ln(10)

    # Header
    for col in df.columns:
        pdf.cell(35, 10, str(col), border=1)
    pdf.ln()

    # Data baris
    for _, row in df.iterrows():
        for item in row:
            pdf.cell(35, 10, str(item), border=1)
        pdf.ln()

    pdf.output(output_path)
    return output_path

# Fungsi khusus tiap modul
def generate_keuangan_pdf():
    if os.path.exists(KEUANGAN_CSV):
        df = pd.read_csv(KEUANGAN_CSV)
        if not df.empty:
            return export_to_pdf("Laporan Keuangan", df, "laporan_keuangan.pdf")
    return None

def generate_proyek_pdf():
    if os.path.exists(PROYEK_CSV):
        df = pd.read_csv(PROYEK_CSV)
        if not df.empty:
            return export_to_pdf("Laporan Proyek", df, "laporan_proyek.pdf")
    return None

def generate_karyawan_pdf():
    if os.path.exists(KARYAWAN_CSV):
        df = pd.read_csv(KARYAWAN_CSV)
        if not df.empty:
            return export_to_pdf("Laporan Karyawan", df, "laporan_karyawan.pdf")
    return None


import pandas as pd
from fpdf import FPDF
import os

DATA_DIR = "data"
KEUANGAN_CSV = os.path.join(DATA_DIR, "keuangan.csv")

def load_data(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame()

def generate_keuangan_pdf(output_path="laporan_keuangan.pdf"):
    df = load_data(KEUANGAN_CSV)
    if df.empty:
        return None

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Laporan Keuangan", ln=True, align="C")
    pdf.ln(10)

    headers = ["Tanggal", "Jenis", "Kategori", "Jumlah", "Keterangan"]
    col_widths = [30, 30, 30, 30, 60]

    for header, width in zip(headers, col_widths):
        pdf.cell(width, 10, header, border=1)
    pdf.ln()

    for _, row in df.iterrows():
        pdf.cell(col_widths[0], 10, str(row['tanggal']), border=1)
        pdf.cell(col_widths[1], 10, row['jenis'], border=1)
        pdf.cell(col_widths[2], 10, row['kategori'], border=1)
        pdf.cell(col_widths[3], 10, str(row['jumlah']), border=1)
        pdf.cell(col_widths[4], 10, row['keterangan'], border=1)
        pdf.ln()

    pdf.output(output_path)
    return output_path

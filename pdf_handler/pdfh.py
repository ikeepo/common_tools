from pypdf import PdfWriter, PdfReader
import yaml
from pathlib import Path

# import fitz
# from ironpdf import *
import shutil
import subprocess
import os


def load_from_yaml():
    dp_pwd = Path(__file__).parent
    yaml_file_path = dp_pwd / "config.yaml"
    with open(yaml_file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data


def merge_files():
    data = load_from_yaml()
    dp_src = data.get("dp_src", ".")
    dp_output = data.get("dp_output", ".")
    pdf_files = data.get("pdf_files", [])
    fn_output = data.get("fn_output", "merged.pdf")

    merger = PdfWriter()
    for pdf in pdf_files:
        pdf_fn = f"{dp_src}/{pdf}"
        merger.append(pdf_fn)
    fp_output = f"{dp_output}/{fn_output}"
    merger.write(fp_output)
    merger.close()
    print(f"PDF files merged successfully as {fp_output}")


def compress_pdf(power=2):
    """Function to compress PDF via Ghostscript command line interface
    From https://github.com/theeko74/pdfc/blob/master/pdf_compressor.py
    """
    # 读取输入 PDF
    data = load_from_yaml()
    dp_src = data.get("dp_src", ".")
    dp_output = data.get("dp_output", ".")
    pdf_compress = data.get("pdf_compress", "NotFind")
    output_fn = data.get("fn_output", f"{pdf_compress}_compressed_{power}.pdf")
    output_file_path = f"{dp_output}/{output_fn}"
    input_file_path = f"{dp_src}/{pdf_compress}"

    print(input_file_path)
    print(output_file_path)
    print(power)
    # exit()

    quality = {0: "/default", 1: "/prepress", 2: "/printer", 3: "/ebook", 4: "/screen"}

    # Basic controls
    # Check if valid path
    if not os.path.isfile(input_file_path):
        print("Error: invalid path for input PDF file.", input_file_path)
        sys.exit(1)

    # Check compression level
    if power < 0 or power > len(quality) - 1:
        print("Error: invalid compression level, run pdfc -h for options.", power)
        sys.exit(1)

    # Check if file is a PDF by extension
    if input_file_path.split(".")[-1].lower() != "pdf":
        print(f"Error: input file is not a PDF.", input_file_path)
        sys.exit(1)

    gs = get_ghostscript_path()
    print("Compress PDF...")
    print(gs)
    initial_size = os.path.getsize(input_file_path)
    subprocess.call(
        [
            gs,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS={}".format(quality[power]),
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            "-sOutputFile={}".format(output_file_path),
            input_file_path,
        ]
    )
    final_size = os.path.getsize(output_file_path)
    ratio = 1 - (final_size / initial_size)
    print("Compression by {0:.0%}.".format(ratio))
    print("Final file size is {0:.5f}MB".format(final_size / 1000000))
    print("Done.")


def get_ghostscript_path():
    gs_names = ["gs", "gswin32", "gswin64"]
    for name in gs_names:
        if shutil.which(name):
            return shutil.which(name)
    raise FileNotFoundError(
        f"No GhostScript executable was found on path ({'/'.join(gs_names)})"
    )


if __name__ == "__main__":
    # merge_files()

    compress_pdf()

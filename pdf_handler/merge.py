from pypdf import PdfWriter
import yaml
from pathlib import Path
def load_from_yaml():
    dp_pwd = Path(__file__).parent
    yaml_file_path = dp_pwd / 'urls.yaml'
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data
def merge_files():
    data = load_from_yaml()
    dp_src = data.get('dp_src', '.')
    dp_output = data.get("dp_output", '.')
    pdf_files = data.get('pdf_files', [])
    fn_output = data.get('fn_output', "merged.pdf")

    merger = PdfWriter()
    for pdf in pdf_files:
        pdf_fn = f"{dp_src}/{pdf}"
        merger.append(pdf_fn)
    fp_output = f"{dp_output}/{fn_output}"
    merger.write(fp_output)
    merger.close()
    print(f"PDF files merged successfully as {fp_output}")

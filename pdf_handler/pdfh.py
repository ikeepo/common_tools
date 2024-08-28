from pypdf import PdfWriter, PdfReader
import yaml
from pathlib import Path
import fitz

def load_from_yaml():
    dp_pwd = Path(__file__).parent
    yaml_file_path = dp_pwd / 'config.yaml'
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

def compress_pdf(compression_ratio):
    # 读取输入 PDF
    data = load_from_yaml()
    dp_src = data.get('dp_src', '.')
    dp_output = data.get("dp_output", '.')
    pdf_compress = data.get('pdf_compress', 'NotFind')
    output_pdf = data.get('fn_output', f"{pdf_compress}_compressed_{compression_ratio}.pdf")
    input_pdf= f"{dp_src}/{pdf_compress}"
    # Open the input PDF file
    pdf_document = fitz.open(input_pdf)
    
    # Get the total number of pages
    num_pages = pdf_document.page_count
    
    # Iterate through each page
    for page_number in range(num_pages):
        page = pdf_document.load_page(page_number)
        
        # Get images on the page
        images = page.get_images(full=True)
        
        for img in images:
            xref = img[0]
            pix = fitz.Pixmap(pdf_document, xref)
            
            # Compress the image
            if pix.n < 5:  # this is GRAY or RGB
                pix = fitz.Pixmap(fitz.csRGB, pix)  # convert to RGB
            pix.set_dpi(int(pix.xres * compression_ratio), int(pix.yres * compression_ratio))
            pdf_document.update_image(xref, pix)
    
    # Save the compressed PDF
    pdf_document.save(output_pdf, garbage=4)
    pdf_document.close()


if __name__=="__main__":
    #merge_files()
    
    compress_pdf(compression_ratio=9.5)

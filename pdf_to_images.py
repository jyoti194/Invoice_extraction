

import os
from pdf2image import convert_from_path

def convert_pdfs_to_images(pdf_folder, output_dir, poppler_path=None):
    """Converts all PDF files in a given folder to images.

    Args:
        pdf_folder: The path to the folder containing PDF files.
        output_dir: The path to the output directory for images.
        poppler_path: Optional path to the Poppler binaries.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)

            try:
                pages = convert_from_path(pdf_path, poppler_path=poppler_path)
                for i, page in enumerate(pages):
                    image_path = os.path.join(output_dir, f"{os.path.splitext(pdf_file)[0]}_page_{i+1}.jpg")
                    page.save(image_path, 'JPEG')
            except Exception as e:
                print(f"Error converting {pdf_file}: {e}")

# Example usage
pdf_folder = r"C:\Users\jyoti\Desktop\pdfs"
output_dir = r"C:\Users\jyoti\Desktop\imgs"
poppler_path = r"C:\Users\jyoti\Downloads\Release-24.02.0-0\poppler-24.02.0\Library\bin"  # Optional, if needed

convert_pdfs_to_images(pdf_folder, output_dir, poppler_path=poppler_path)

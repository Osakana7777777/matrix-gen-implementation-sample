import pypdf
import sys

def extract_text(pdf_path):
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        # Read last 5 pages
        total_pages = len(reader.pages)
        start_page = max(0, total_pages - 5)
        for i in range(start_page, total_pages):
            text += f"--- Page {i+1} ---\n"
            text += reader.pages[i].extract_text() + "\n"
        return text
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    pdf_path = "2410.14251v2.pdf"
    print(extract_text(pdf_path))

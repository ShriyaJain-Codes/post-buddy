import pytesseract
from PIL import Image
import fitz  # PyMuPDF

# If needed, set Tesseract path (only if not in PATH):
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def test_image():
    try:
        img = Image.open("sample.png")  # <-- put any small PNG in this folder
        text = pytesseract.image_to_string(img)
        print("[IMAGE OCR RESULT]")
        print(text if text.strip() else "[NO TEXT DETECTED]")
    except Exception as e:
        print("[ERROR in IMAGE OCR]", e)

def test_pdf():
    try:
        doc = fitz.open("sample.pdf")  # <-- put any PDF in this folder
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            print(f"[PDF PAGE {page_num+1} TEXT LAYER]")
            print(text.strip() if text.strip() else "[NO TEXT, OCR needed]")
    except Exception as e:
        print("[ERROR in PDF OCR]", e)

if __name__ == "__main__":
    test_image()
    test_pdf()

import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import fitz            # PyMuPDF
from pdf2image import convert_from_path

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

POPPLER_PATH = None  # set path if needed
ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".pdf"}

# ------------------- Helpers -------------------

def allowed_file(filename):
    ext = os.path.splitext(filename.lower())[1]
    return ext in ALLOWED_EXT

def preprocess_pil_image(pil_img):
    img = pil_img.convert("L")
    img = img.filter(ImageFilter.SHARPEN)
    img = ImageEnhance.Contrast(img).enhance(1.5)
    return img

def ocr_image_pil(pil_img):
    img = preprocess_pil_image(pil_img)
    try:
        text = pytesseract.image_to_string(img, lang="eng", config="--oem 1 --psm 3")
        return text.strip()
    except Exception as e:
        print("OCR error:", e)
        return ""

def extract_text_from_pdf_with_textlayer(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        full_text = [page.get_text("text") or "" for page in doc]
        return "\n".join(full_text).strip()
    except Exception as e:
        print("PyMuPDF extraction error:", e)
        return ""

def extract_text_from_pdf_with_ocr(pdf_path, dpi=300):
    text_parts = []
    try:
        if POPPLER_PATH:
            pages = convert_from_path(pdf_path, dpi=dpi, poppler_path=POPPLER_PATH)
        else:
            pages = convert_from_path(pdf_path, dpi=dpi)
        for pil_page in pages:
            text_parts.append(ocr_image_pil(pil_page))
        return "\n".join(text_parts).strip()
    except Exception as e:
        print("PDF->image OCR error:", e)
        return ""

def describe_image(pil_img):
    """
    Placeholder description for images without text.
    """
    return "An engaging social media image (no text detected)."

# ------------------- Flask routes -------------------

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(f.filename):
        return jsonify({"error": "Unsupported file type. Allowed: png,jpg,jpeg,pdf"}), 400

    filename = secure_filename(f.filename)
    saved_path = os.path.join(UPLOAD_FOLDER, filename)
    f.save(saved_path)

    ext = os.path.splitext(filename.lower())[1]

    try:
        text = ""
        display_text = ""
        word_count = 0
        char_count = 0

        if ext == ".pdf":
            text = extract_text_from_pdf_with_textlayer(saved_path)
            if not text.strip():
                text = extract_text_from_pdf_with_ocr(saved_path)
            display_text = text if text else "No text detected in PDF."
        else:
            pil_img = Image.open(saved_path)
            text = ocr_image_pil(pil_img)
            if not text:
                display_text = describe_image(pil_img)
            else:
                display_text = text

        # Compute word/char count only if OCR text exists
        if text:
            words = [w for w in text.split() if w.strip()]
            word_count = len(words)
            char_count = len(text)

        # Engagement suggestions
        suggestions = []
        if word_count < 8:
            suggestions.append("Post is very short — add a clear benefit or detail.")
        if word_count > 60:
            suggestions.append("Post is long — consider trimming to main point (10–40 words).")
        if "#" not in display_text:
            suggestions.append("Consider adding 2–3 relevant hashtags for better reach.")
        if not any(kw in display_text.lower() for kw in ["join", "learn", "follow", "watch", "check"]):
            suggestions.append("Add a gentle call-to-action (e.g., 'Learn more', 'Join us', 'Follow').")

        result = {
            "text": display_text,
            "word_count": word_count,
            "char_count": char_count,
            "suggestions": suggestions
        }

        return jsonify(result), 200

    except Exception as e:
        print("Processing error:", e)
        return jsonify({"error": f"Processing failed: {e}"}), 500

# ------------------- Run -------------------

if __name__ == "__main__":
    app.run(debug=True)


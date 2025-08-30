# Post Buddy

📊 **Social Media Post Analyzer**  
Analyze PDFs or images to extract text, count words/characters, and get engagement suggestions.

## Installation

1. Clone the repo:  
   `git clone https://github.com/<your-username>/post-buddy.git`  
2. Navigate to project folder:  
   `cd post-buddy`  
3. Create virtual environment (optional):  
   `python -m venv venv`  
   Activate it:  
   - Windows: `venv\Scripts\activate`  
   - Mac/Linux: `source venv/bin/activate`  
4. Install dependencies:  
   `pip install -r requirements.txt`  
5. Run locally:  
   `python app.py`  

## Usage

- Open browser at `http://127.0.0.1:5000`  
- Upload PDF or image  
- View word count, character count, extracted text, and engagement suggestions  

## Live App

Try it here: [https://post-buddy.onrender.com](https://post-buddy.onrender.com)

## Features

- PDF & image text extraction (OCR via Tesseract)  
- Word and character count  
- AI fallback for images without text  
- Engagement improvement suggestions  

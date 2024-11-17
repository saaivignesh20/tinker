import pytesseract
import io
import pandas as pd
from PIL import Image
from pypdf import PdfReader


def read_from_pdf(path):
    '''Reads a PDF file from path and returns the text content.'''
    reader = PdfReader(path)
    text = ""
    for idx in range(len(reader.pages)):
        page = reader.pages[idx]
        text += page.extract_text()
        # Process images in the PDF if any
        if page.images:
            for img in page.images:
                image = Image.open(io.BytesIO(img.data))
                text += read_from_image(image=image)
    return text


def read_from_image(path=None, image=None):
    '''Reads an image file from path or image and returns the text content.'''
    if path:
        return pytesseract.image_to_string(Image.open(path))
    if image:
        return pytesseract.image_to_string(image)


def read_from_excel(path):
    '''Reads an Excel file from path and returns the content as text.'''
    df = pd.read_excel(path)
    return df.to_string()

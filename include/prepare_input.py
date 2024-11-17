# import libraries
import pytesseract
from pypdf import PdfReader
import os
from pdf2image import convert_from_path
import pandas as pd
from PIL import Image
from texify.inference import batch_inference
from texify.model.model import load_model
from texify.model.processor import load_processor
model = load_model()
processor = load_processor()


def read_from_pdf(path):
    '''Reads a PDF file from path and returns as text content.'''
    reader = PdfReader(path)
    text = ""
    for i in range(len(reader.pages)):
        p = reader.pages[i]
        text += p.extract_text()
    return text


def read_from_image(path):
    '''Reads an image file from path and returns as text content.'''
    return pytesseract.image_to_string(Image.open(path))


def read_from_excel(path):
    '''Reads an excel file from path and returns as text content.'''
    df = pd.read_excel(path)
    return df.to_string()


# dir = os.path.dirname(os.path.dirname(__file__))
# print(read_from_pdf(f"{dir}/input/Q4-taylor.pdf"))

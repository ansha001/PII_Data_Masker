import cv2
import spacy
import re
import easyocr
from IPython.display import display, Image

nlp = spacy.load('en_core_web_sm')
reader = easyocr.Reader(['en'])

def recognize_text(img_path):
    '''Loads an image and recognizes text.'''
    return reader.readtext(img_path)

def nerr_rrr(text):
    entities = ["PERSON", "DATE", "GPE", "MONEY", "PERCENT", "TIME", "QUANTITY", "ORDINAL", "NORP"]

    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    phi_pattern = {
        r"\b\d{16}\b": "Credit/Debit Card Number",
        r"\b[A-Za-z]{2}\d{6}\b": "Employee ID",
    }

    pii_offsets = []
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in entities:
            pii_offsets.extend(range(ent.start_char, ent.end_char))

    # Replace only the identified PII entities with blackout characters
    redacted_text = ""
    for i, char in enumerate(text):
        if i in pii_offsets or re.match(email_pattern, char):
            redacted_text += "*"
        else:
            redacted_text += char

    return redacted_text

def overlay_ocr_text(img_path, vertical_offset=0):
    '''Loads an image, recognizes text, and overlays the text on the image.'''
    img = cv2.imread(img_path)

    result = recognize_text(img_path)

    for (bbox, text, prob) in result:
        if prob >= 0.5:
            t = nerr_rrr(text)
            print(t)
            lst = []

            for letter in t:
                lst.append(letter)
                if(lst[0]=="*"):

                        # Overlay text on image
                        (top_left, top_right, bottom_right, bottom_left) = bbox
                        top_left = (int(top_left[0]), int(top_left[1]) + vertical_offset)
                        bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
                        font = cv2.FONT_HERSHEY_SIMPLEX

                        # Draw a filled rectangle as background for the text
                        img = cv2.rectangle(img, top_left, bottom_right, (0, 0, 0), -1)

    temp_img_path = "static/public/masked_image.jpg"
    cv2.imwrite(temp_img_path, img)
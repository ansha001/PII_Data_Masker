#!pip install -U spacy
#!python -m spacy download en_core_web_sm

import spacy
from spacy import displacy

from termcolor import colored
import random
import re

nlp = spacy.load('en_core_web_sm')

# def replace_ners(text, replacements):
#     doc = nlp(text)
#     regex_email = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
#     replaced_text = text
#     replaced_entities = set()    
#     doc = nlp(text)
#     for txt in doc:
#         if re.match(regex_email, txt.text):
#             alternative = random.choice(replacements['EMAIL'])
#             temp = colored(alternative, 'blue')
#             temp1 = colored(txt.text, 'red')
#             text = text.replace(txt.text, temp1)
#             replaced_text = replaced_text.replace(txt.text, temp)
#     for ent in doc.ents:
#         if ent.label_ in replacements and ent.text not in replaced_entities:
#             alternative = random.choice(replacements[ent.label_])
#             temp = colored(alternative, 'green')
#             temp1 = colored(ent.text, 'red')
#             text = text.replace(ent.text, temp1)
#             replaced_text = replaced_text.replace(ent.text, temp)
#             replaced_entities.add(ent.text)
#         else:
#             pass
    
#     # Remove color codes from the obfuscated text
#     plain_text = re.sub('\x1b\[\d+m', '', text)
#     plain_replaced_text = re.sub('\x1b\[\d+m', '', replaced_text)    
#     return plain_replaced_text


def replace_ners(text, replacements):
    doc = nlp(text)
    regex_email = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    replaced_text = text
    replaced_entities = set()
    doc = nlp(text)
    for txt in doc:
        if re.match(regex_email, txt.text):
            alternative = random.choice(replacements['EMAIL'])
            temp = f'<span style="color: blue;">{txt.text}</span>'
            temp1 = f'<span style="color: red;">{txt.text}</span>'
            text = text.replace(txt.text, temp1)
            replaced_text = replaced_text.replace(txt.text, temp)
    for ent in doc.ents:
        if ent.label_ in replacements and ent.text not in replaced_entities:
            alternative = random.choice(replacements[ent.label_])
            temp = f'<span style="color: blue;">{alternative}</span>'
            temp1 = f'<span style="color: red;">{ent.text}</span>'
            text = text.replace(ent.text, temp1)
            replaced_text = replaced_text.replace(ent.text, temp)
            replaced_entities.add(ent.text)
        else:
            pass

    # Remove color codes from the obfuscated text
    plain_text = re.sub('\x1b\[\d+m', '', text)
    plain_replaced_text = re.sub('\x1b\[\d+m', '', replaced_text)
    return plain_replaced_text


# Dictionary of replacements for NERs
ner_replacements = {
    'PERSON': ['Michael', 'David', 'Sarah',"Anna","Anita","Leo","Matt","Arnold","Bob","James","Steve","John"],
    'NORP': ['Americans', 'Canadians', 'Germans',"Indians","Italians","Greeks","British","Koreans","Japanese","Russians"],
    'FAC': ['museum', 'stadium', 'theater',"studio","college","university"],
    'ORG': ['Google', 'Apple', 'Amazon',"Samsung","Nokia","IBM","Facebook","Twitter","Boeing"],
    'GPE': ['London', 'Paris', 'Berlin',"New York","Sydney","Singapore","Tokyo","Hongkong"],
    'LOC': ['beach', 'mountain', 'forest'],
    'PRODUCT': ['phone', 'car', 'laptop',"cycle","television","chair","sofa","fan"],
    'EVENT': ['conference', 'festival', 'exhibition',"birthday","marraige","hackathon"],
    'DATE': ['tomorrow', 'next week', 'in July','today','day after','last week','in May','next month'],
    'TIME': ['morning', 'afternoon', 'evening','night'],
    'MONEY': ['$100', '$50.75', '€20','$99','$23'],
    'PERCENT': ['20%', '50%', '75%','100%'],
    'QUANTITY': ['10 kg', '3 liters', '5 miles','12 pounds','15 miles','12 gallon'],
    'ORDINAL': ['first', 'second', 'third','fourth','fifth'],
    'CARDINAL': ['one', 'two', 'three','four','five'],
    'EMAIL':['xyz@abc.com','pqr@abc.com','iam@xyz.com','nothing@xyz.com'],
    "MEDICAL RECORD NUMBER":['MRN00000000',"MRN********","MRNXXXXXXXX"]
}


# Define the entities to extract NER tags for
entities = ["PERSON", "DATE", "ORG", "GPE", "MONEY", "PERCENT", "NORP"]

email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

# Define the PHI patterns for redaction
phi_patterns = {
    r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b": "Patient name",
    r"\b\d{2}/\d{2}/\d{4}\b": "Date of Birth",
    r"\b[A-Z]{2}\d{8}\b": "Medical Record Number",
    r"\b\d{3}-\d{2}-\d{4}\b": "Social Security Number",
    r"\b\d{10}\b": "Health Plan Beneficiary Number",
    r"\b\d{10}\b": "Account Number",
    r"\b[A-Z]{3}\d{6}\b": "Certificate/License Number",
    r"\b[A-Z]{3}\d{3}\b": "Vehicle Identifier",
    r"\b[A-Z]{3}\d{3}\b": "Device Identifier",
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b": "IP Address",
    r"\b\w+\s(?:Fingerprint|Voiceprints)\b": "Biometric Identifier",
    r"\b\d{5}\b": "Any Unique Identifying Number",
    r"\[REDACTED\]": "Finger or Voiceprints",
    r"\bEIN\d{6}\b": "Employer Identifier",
    r"\(\d{3}\) \d{3}-\d{4}": "Telephone Number",
    r"\b[\w\.-]+@[\w\.-]+\.\w+\b": "Email",
    r"\b\d{16}\b": "Credit/Debit Card Number",
    r"\b[A-Za-z]{2}\d{6}\b": "Employee ID",
}


def mask(text):
    blackout_char = "*"
    doc = nlp(text)

    # Replace the identified PHI patterns with blackout characters
    redacted_text = text
    for pattern, _ in phi_patterns.items():
        redacted_text = re.sub(pattern,"******", redacted_text)

    #Replace the identified entities and email addresses with blackout characters
    doc  = nlp(redacted_text)
    blackout_text = ""
    for token in doc:
        if token.ent_type_ in entities or re.match(email_pattern, token.text):
            blackout_text += blackout_char * len(token.text) + " "
        else:
            blackout_text += token.text + " "

    return blackout_text


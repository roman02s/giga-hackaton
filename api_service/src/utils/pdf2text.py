import re

import pdfplumber


def get_symbols2chars(text, chars):
    new_text = ""
    for line in text.split("\n"):
        new_text += re.sub(" +", " ", line.strip())
        if line.strip():
            new_text += " "
    alphabet = "zxcvbasdfgqwertnmhjklyuiop1234567890-+=/*©()[]"
    symbols2chars = []
    i = 0
    j = 0
    while i < len(new_text) and j < len(chars):
        if new_text[i] == " ":
            symbols2chars.append(" ")
            i += 1
        elif new_text[i] == "\n":
            symbols2chars.append("\n")
            i += 1
        elif chars[j]["text"].lower() not in alphabet:
            j += 1
        elif new_text[i].lower() not in alphabet:
            symbols2chars.append(new_text[i])
            i += 1
        elif new_text[i].lower() != chars[j]["text"].lower():
            symbols2chars.append(new_text[i])
            i += 1
        else:
            symbols2chars.append(chars[j])
            i += 1
            j += 1
    return symbols2chars


def extract_text_from_pdf(pdf_path):
    extracted_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Использование layout=True и use_text_flow=True для сохранения форматирования текста
            text = page.extract_text(
                x_tolerance=2, y_tolerance=3, layout=True, use_text_flow=True
            )
            if text:  # Проверка на наличие текста на странице
                chars = page.chars  # Получаем список символов на странице
                symbols2chars = get_symbols2chars(text, chars)
                for char in symbols2chars:
                    if isinstance(char, str):
                        extracted_text += char
                    else:
                        extracted_text += char["text"]
                extracted_text += "\n"

    pattern = r"References.*"
    trimmed_text = re.sub(pattern, "References", extracted_text, flags=re.DOTALL)
    return trimmed_text

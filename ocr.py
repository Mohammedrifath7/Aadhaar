import pytesseract
import cv2
import re

# Uncomment if needed on Windows
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray)


def extract_aadhaar_details(image_path):
    text = extract_text(image_path)

    aadhaar_no = re.findall(r"\d{4}\s\d{4}\s\d{4}", text)

    dob = re.findall(r"\d{2}/\d{2}/\d{4}", text)

    gender = None
    if "MALE" in text.upper():
        gender = "Male"
    elif "FEMALE" in text.upper():
        gender = "Female"

    # Name heuristic (line before DOB usually)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    name = None
    for i, line in enumerate(lines):
        if "DOB" in line or "Date of Birth" in line:
            if i > 0:
                name = lines[i - 1]
            break

    return {
        "name": name or "",
        "dob": dob[0] if dob else "",
        "gender": gender or "",
        "aadhaar": aadhaar_no[0] if aadhaar_no else ""
    }


def extract_pan_details(image_path):
    text = extract_text(image_path).upper()

    pan_no = re.findall(r"[A-Z]{5}[0-9]{4}[A-Z]", text)

    dob = re.findall(r"\d{2}/\d{2}/\d{4}", text)

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    name = ""
    father_name = ""

    # PAN cards usually follow:
    # NAME
    # FATHER NAME
    # DOB
    if len(lines) >= 3:
        name = lines[0]
        father_name = lines[1]

    return {
        "name": name,
        "father_name": father_name,
        "dob": dob[0] if dob else "",
        "pan": pan_no[0] if pan_no else ""
    }

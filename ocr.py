import pytesseract
import cv2
import re

def extract_text_safe(image_path):
    try:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return pytesseract.image_to_string(gray)
    except Exception:
        # Tesseract not available (Streamlit Cloud)
        return ""


def extract_aadhaar_details(image_path):
    text = extract_text_safe(image_path)

    aadhaar = re.findall(r"\d{4}\s\d{4}\s\d{4}", text)
    dob = re.findall(r"\d{2}/\d{2}/\d{4}", text)

    gender = ""
    if "MALE" in text.upper():
        gender = "Male"
    elif "FEMALE" in text.upper():
        gender = "Female"

    # name heuristic
    name = ""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for i, line in enumerate(lines):
        if "DOB" in line or "Date of Birth" in line:
            if i > 0:
                name = lines[i - 1]
            break

    return {
        "name": name,
        "dob": dob[0] if dob else "",
        "gender": gender,
        "aadhaar": aadhaar[0] if aadhaar else ""
    }


def extract_pan_details(image_path):
    text = extract_text_safe(image_path).upper()

    pan = re.findall(r"[A-Z]{5}[0-9]{4}[A-Z]", text)
    dob = re.findall(r"\d{2}/\d{2}/\d{4}", text)

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    name = lines[0] if len(lines) > 0 else ""
    father = lines[1] if len(lines) > 1 else ""

    return {
        "name": name,
        "father_name": father,
        "dob": dob[0] if dob else "",
        "pan": pan[0] if pan else ""
    }

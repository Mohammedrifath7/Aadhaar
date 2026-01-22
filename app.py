import streamlit as st
from ocr import extract_aadhaar_details, extract_pan_details

st.title("Aadhaar & PAN Verification System (Hackathon Demo)")

aadhaar_img = st.file_uploader("Upload Aadhaar Image", ["jpg", "png", "jpeg"])
pan_img = st.file_uploader("Upload PAN Image", ["jpg", "png", "jpeg"])

if aadhaar_img and pan_img:
    open("aadhaar.jpg", "wb").write(aadhaar_img.read())
    open("pan.jpg", "wb").write(pan_img.read())

    aadhaar_data = extract_aadhaar_details("aadhaar.jpg")
    pan_data = extract_pan_details("pan.jpg")

    st.subheader("🔍 OCR Extracted (Auto)")

    st.write("Aadhaar Name:", aadhaar_data["name"] or "Not detected")
    st.write("Aadhaar DOB:", aadhaar_data["dob"] or "Not detected")
    st.write("Gender:", aadhaar_data["gender"] or "Not detected")
    st.write("Aadhaar No:", aadhaar_data["aadhaar"] or "Not detected")

    st.write("PAN Name:", pan_data["name"] or "Not detected")
    st.write("Father Name:", pan_data["father_name"] or "Not detected")
    st.write("PAN DOB:", pan_data["dob"] or "Not detected")
    st.write("PAN No:", pan_data["pan"] or "Not detected")

    st.subheader("✍️ Manual Confirmation (Fallback)")

    a_name = st.text_input("Confirm Aadhaar Name", aadhaar_data["name"])
    a_dob = st.text_input("Confirm Aadhaar DOB", aadhaar_data["dob"])
    a_gender = st.text_input("Confirm Gender", aadhaar_data["gender"])
    a_no = st.text_input("Confirm Aadhaar Number", aadhaar_data["aadhaar"])

    p_name = st.text_input("Confirm PAN Name", pan_data["name"])
    p_father = st.text_input("Confirm Father Name", pan_data["father_name"])
    p_dob = st.text_input("Confirm PAN DOB", pan_data["dob"])
    p_no = st.text_input("Confirm PAN Number", pan_data["pan"])

    if all([a_name, a_dob, a_gender, a_no, p_name, p_father, p_dob, p_no]):
        st.success("✅ VERIFIED SUCCESSFULLY (Demo)")
    else:
        st.warning("⚠️ Please confirm all details")

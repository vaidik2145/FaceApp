
import requests
import streamlit as st
from PIL import Image
import io

def compare_faces(api_key, api_secret, image_file1, image_file2):
    url = "https://api-us.faceplusplus.com/facepp/v3/compare"
    
    image_bytes1 = image_file1.read()
    image_bytes2 = image_file2.read()
    
    files = {
        "image_file1": (image_file1.name, image_bytes1, "image/jpeg" if image_file1.type == "image/jpeg" else "image/png"),
        "image_file2": (image_file2.name, image_bytes2, "image/jpeg" if image_file2.type == "image/jpeg" else "image/png")
    }
    
    data = {
        "api_key": api_key,
        "api_secret": api_secret
    }
    
    response = requests.post(url, files=files, data=data)
    
    return response.json()

st.title("Face Comparison Application")

API_KEY = "7thFhdOYTWoVZ2vM669zgZGnpQMkjvqo"
API_SECRET = "uUQr90A3iPF912qSIFO9uvbe-yiWq0iz"

uploaded_file1 = st.file_uploader("Upload First Image", type=["jpg", "jpeg", "png"])
uploaded_file2 = st.file_uploader("Upload Second Image", type=["jpg", "jpeg", "png"])

if uploaded_file1 and uploaded_file2:
    image1 = Image.open(uploaded_file1)
    image2 = Image.open(uploaded_file2)
    
    st.image([image1, image2], caption=["First Image", "Second Image"], width=250)
    
    if st.button("Compare Faces"):
        uploaded_file1.seek(0)  # Reset file pointer
        uploaded_file2.seek(0)
        result = compare_faces(API_KEY, API_SECRET, uploaded_file1, uploaded_file2)
        
        confidence = result.get("confidence", 0)
        threshold = result.get("thresholds", {}).get("1e-5", 0)
        
        if confidence >= threshold:
            st.success(f"Match Found! Confidence: {confidence:.2f}%")
        else:
            st.error(f"No Match. Confidence: {confidence:.2f}%")
        
        st.json(result)

if __name__ == "__main__":
    st.write("Upload two images to compare faces.")

# Main Code 

import streamlit as st
from skimage.metrics import structural_similarity
import imutils
import cv2
import numpy as np
from PIL import Image
import tempfile
from fpdf import FPDF


def create_pdf_report(original_image_np, tampered_image_np, score, threshold, suggestions):
    pdf = FPDF()
    pdf.add_page()

    # Title 
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "PAN Card Tampering Detection Report", 0, 1, "C")
    
    # SSIM Score
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"SSIM Score: {score:.4f}", 0, 1)
    pdf.cell(0, 10, f"Threshold for Authenticity: {threshold:.2f}", 0, 1)

    # Authenticity Decision
    decision = "REAL" if score > threshold else "FAKE"
    pdf.cell(0, 10, f"Conclusion: The PAN card is considered {decision}.", 0, 1, "L")

    # Suggestions for Image Quality
    if suggestions:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Suggestions for Image Quality Improvement:", 0, 1)
        pdf.set_font("Arial", "", 12)
        for suggestion in suggestions:
            pdf.cell(0, 10, f"- {suggestion}", 0, 1)

    # Save images temporarily and add to PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_original, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_tampered:
        # Save the images as temporary files
        cv2.imwrite(temp_original.name, original_image_np)
        cv2.imwrite(temp_tampered.name, tampered_image_np)

        # Add images to the PDF
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Original Image with Detected Areas", 0, 1)
        pdf.image(temp_original.name, x=10, y=pdf.get_y(), w=90)
        pdf.cell(0, 10, "", 0, 1)  # Spacer
        pdf.cell(0, 10, "Tampered Image with Detected Areas", 0, 1)
        pdf.image(temp_tampered.name, x=10, y=pdf.get_y(), w=90)

    # Save PDF temporarily and return path
    temp_pdf_path = tempfile.mktemp(suffix=".pdf")
    pdf.output(temp_pdf_path)
    return temp_pdf_path


def main():
    # Enhanced main title with background and animation
    st.markdown("""
        <style>
        .main-title {
            background-color: #4CAF50;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-size: 32px;
            font-weight: bold;
        }
        
  
        </style>
        <div class="main-title">PAN-Card Tampering Detection</div>
        <p style='text-align: center; color: #808080;'>Upload and compare two images to detect any modifications.</p>
    """, unsafe_allow_html=True)

    # Sidebar settings
    st.sidebar.header("Settings")
    color = st.sidebar.color_picker("Choose a color for highlighting differences", "#FF0000")
    threshold_value = st.sidebar.slider("SSIM Score Threshold", 0.0, 1.0, 0.8, 0.01)

    # Image upload
    st.subheader("Upload the Original and Tampered Images")
    original_file = st.file_uploader("Upload Original Image", type=['png', 'jpg', 'jpeg'])
    tampered_file = st.file_uploader("Upload Tampered Image", type=['png', 'jpg', 'jpeg'])

    if original_file and tampered_file:
        # Load images
        original = Image.open(original_file)
        tampered = Image.open(tampered_file)

        # Convert to numpy arrays
        original_np = cv2.cvtColor(np.array(original), cv2.COLOR_RGB2BGR)
        tampered_np = cv2.cvtColor(np.array(tampered), cv2.COLOR_RGB2BGR)

        # Convert images to grayscale
        original_gray = cv2.cvtColor(original_np, cv2.COLOR_BGR2GRAY)
        tampered_gray = cv2.cvtColor(tampered_np, cv2.COLOR_BGR2GRAY)

        # Compute SSIM
        (score, diff) = structural_similarity(original_gray, tampered_gray, full=True)
        diff = (diff * 255).astype("uint8")

        # Threshold and find contours
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # Draw rectangles around detected areas with chosen color
        contour_color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(original_np, (x, y), (x + w, y + h), contour_color, 2)
            cv2.rectangle(tampered_np, (x, y), (x + w, y + h), contour_color, 2)

        # Display images with contours
        st.markdown("<h3 style='color: #4CAF50;'>Original Image with Detected Areas</h3>", unsafe_allow_html=True)
        st.image(original_np, channels='BGR')
        
        st.markdown("<h3 style='color: #4CAF50;'>Tampered Image with Detected Areas</h3>", unsafe_allow_html=True)
        st.image(tampered_np, channels='BGR')
        
        # Display SSIM score
        st.write(f"**SSIM Score:** {score:.4f}")

        # Determine authenticity and suggestions
        suggestions = []
        if score > threshold_value:
            st.success("✅ The given PAN card is **REAL** compared to the original.")
        else:
            st.error("❌ The given PAN card is **FAKE** compared to the original.")
            suggestions.append("Ensure the image is not blurred.")
            suggestions.append("Verify lighting and avoid glare on the card surface.")

        # Generate PDF report
        st.subheader("Download Detailed Report")
        report_path = create_pdf_report(original_np, tampered_np, score, threshold_value, suggestions)
        with open(report_path, "rb") as f:
            st.download_button(label="Download Report as PDF", data=f, file_name="PAN_Card_Report.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()

# PAN Card Tampering Detection

This application helps in detecting tampered PAN card images by comparing an original image with a potentially tampered one. Using the Structural Similarity Index (SSIM), the app calculates the similarity score between the two images and provides conclusions about the authenticity of the PAN card. If the PAN card is considered tampered, suggestions for image quality improvements are provided. The results can be saved in a detailed PDF report.

## Features

- **Image Comparison**: Upload and compare original and tampered images.
- **SSIM Score**: Detect image modifications using SSIM (Structural Similarity Index) score.
- **Tampered Area Detection**: Draw bounding boxes around modified areas in the images.
- **Authenticity Decision**: Display a conclusion (REAL or FAKE) based on the SSIM score.
- **Suggestions**: Provide image quality improvement suggestions if tampering is detected.
- **PDF Report**: Download a detailed PDF report containing the analysis and suggestions.

## Requirements

To run this application, you need Python installed along with the following dependencies:

- `streamlit`
- `opencv-python`
- `imutils`
- `PIL`
- `numpy`
- `skimage`
- `fpdf`

You can install all dependencies using the `requirements.txt` file.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/Sankkkett/PAN-card-tampering-detaction-app.git
    cd PAN-card-tampering-detaction-app
    ```

2. Create a virtual environment:

    ```bash
    python -m /venv 
    ```

3. Activate the virtual environment:
   
   On Windows:
   ```bash
   venv\Scripts\activate

## Author
- **Name**: Sanket Pawar
- **Contact**: [sanketpawar24112001@gmail.com](mailto:sanketpawar24112001@gmail.com)
- **LinkedIn**: [https://www.linkedin.com/in/sanket-pawar-5b6682286/]


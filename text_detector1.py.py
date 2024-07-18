import cv2
import pytesseract
import pandas as pd
import re
import os

# Function to process each image and save extracted data to a CSV file
def process_image(image_path, output_dir):
    # Load the image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Failed to load image: {image_path}")
        return

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply OCR to extract text data with confidence scores
    custom_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(gray, config=custom_config, output_type=pytesseract.Output.DICT)

    # Extract the text and confidence scores
    extracted_text = ' '.join(data['text'])
    conf_data = {data['text'][i].strip(): data['conf'][i] for i in range(len(data['text'])) if data['text'][i].strip()}

    # Define a function to extract fields and their confidence scores
    def extract_fields(text, conf_data):
        fields = {
            "Total Amount": "",
            "Date": "",
            "PO #": "",
            "Invoice #": "",
            "Tax ID": "",
            "Tax": "",
            "Subtotal": "",
            "Shipping": ""
        }
        conf_scores = {
            "Total Amount": 0,
            "Date": 0,
            "PO #": 0,
            "Invoice #": 0,
            "Tax ID": 0,
            "Tax": 0,
            "Subtotal": 0,
            "Shipping": 0
        }

        patterns = {
            "Total Amount": r'\b(Total|TOTAL)\s*(Amount|AMOUNT)?\s*[:#]?\s*\$?\s?(\d+[\d,\.]*)',
            "Date": r'\b(Date|DATE|date|Due Date)\s*[:#]?\s*(\d{4}-\d{2}-\d{2})',
            "PO #": r'\b(PO Number|PO|PO #:|PO #|P\.O\.#|P\.O\. Number|P\.O\.)\s*[:#]?\s*(\S+)',
            "Invoice #": r'\b(Invoice #:|Invoice Number:|Invoice|INVOICE|Invoice #|INVOICE#|Invoice #|INVOICE #)\s*[:#]?\s*(\S+)',
            "Tax ID": r'\b(Tax ID|TAX ID)\s*[:#]?\s*(\S+)',
            "Tax": r'\b(Sales Tax|SalesTax|SALES TAX|TAX)\s*[:#]?\s*\$?\s?(\d+[\d,\.]*)',
            "Subtotal": r'\b(Subtotal|SUBTOTAL|sub total|SUB TOTAL)\s*[:#]?\s*\$?\s?(\d+[\d,\.]*)',
            "Shipping": r'\b(Shipping|SHIPPING|Shipping Charges|SHIPPING CHARGES)\s*[:#]?\s*\$?\s?(\d+[\d,\.]*)'
        }

        for field, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                matched_text = match.group(3) if field == "Total Amount" else match.group(2)
                fields[field] = matched_text
                # Using closest matching text to find the confidence score
                closest_match = min(conf_data.keys(), key=lambda x: len(set(matched_text) - set(x)))
                conf_scores[field] = conf_data.get(closest_match, 0)
            else:
                fields[field] = "No data found"
                conf_scores[field] = 0

        return fields, conf_scores

    # Extract fields and their confidence scores
    fields, conf_scores = extract_fields(extracted_text, conf_data)

    # Convert the fields and confidence scores to a pandas DataFrame
    df = pd.DataFrame({
        "Field": list(fields.keys()),
        "Data": list(fields.values()),
        "Confidence": list(conf_scores.values())
    })

    # Create output file name based on the input image name
    image_name = os.path.basename(image_path)
    output_csv = os.path.join(output_dir, f"{os.path.splitext(image_name)[0]}_extracted_fields.csv")
    df.to_csv(output_csv, index=False)

    print(f"Data has been extracted and saved to {output_csv}")

# Directory to save the output CSV files
output_dir = r"C:\Users\jyoti\Desktop\csvs"
os.makedirs(output_dir, exist_ok=True)

# Directory containing the images
image_dir = r"C:\Users\jyoti\Desktop\imgs"

# Loop through all images in the directory
for image_file in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image_file)
    process_image(image_path, output_dir)

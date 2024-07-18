import cv2
import numpy as np
import pytesseract
import csv
import os

from merge_boxes import make_rows, merge_boxes
from rem_lines import ignore_lines, segment_columns

# Define default labels and synonyms
labels = {
    'total amount': 'Total Amount',
    'total': 'Total Amount',
    'amount due': 'Total Amount',
    'total due': 'Total Amount',
    'date': 'Date',
    'invoice date': 'Date',
    'billing date': 'Date',
    'po number': 'PO Number',
    'purchase order number': 'PO Number',
    'po#': 'PO Number',
    'invoice number': 'Invoice Number',
    'invoice no': 'Invoice Number',
    'inv#': 'Invoice Number',
    'tax id': 'Tax ID',
    'tax identification number': 'Tax ID',
    'tin': 'Tax ID',
    'tax': 'Tax',
    'sales tax': 'Tax',
    'vat': 'Tax',
    'subtotal': 'Subtotal',
    'sub total': 'Subtotal',
    'shipping': 'Shipping Charges',
    'shipping charges': 'Shipping Charges',
    'freight': 'Shipping Charges',
    'delivery': 'Shipping Charges'
}

synonyms = {
    'Total Amount': ['total amount', 'total', 'amount due', 'total due'],
    'Date': ['date', 'invoice date', 'billing date'],
    'PO Number': ['po number', 'purchase order number', 'po#'],
    'Invoice Number': ['invoice number', 'invoice no', 'inv#'],
    'Tax ID': ['tax id', 'tax identification number', 'tin'],
    'Tax': ['tax', 'sales tax', 'vat'],
    'Subtotal': ['subtotal', 'sub total'],
    'Shipping Charges': ['shipping', 'shipping charges', 'freight', 'delivery']
}

expected_fields = [
    'Total Amount', 'Date', 'PO Number', 'Invoice Number',
    'Tax ID', 'Tax', 'Subtotal', 'Shipping Charges'
]

# Helper function for preprocessing the image
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Unable to read image file {image_path}")

    img = cv2.equalizeHist(img)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return img

# Helper function for Levenshtein distance (optional for better text matching)
def levenshtein_ratio_and_distance(s, t, ratio_calc=False):
    rows = len(s) + 1
    cols = len(t) + 1
    distance = np.zeros((rows, cols), dtype=int)

    for i in range(1, rows):
        for k in range(1, cols):
            distance[i][0] = i
            distance[0][k] = k

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0
            else:
                cost = 1
            distance[row][col] = min(distance[row - 1][col] + 1,      # Cost of deletions
                                     distance[row][col - 1] + 1,      # Cost of insertions
                                     distance[row - 1][col - 1] + cost)  # Cost of substitutions

    if ratio_calc:
        Ratio = ((len(s) + len(t)) - distance[row][col]) / (len(s) + len(t))
        return Ratio
    else:
        return f"The strings are {distance[row][col]} edits away"

# Main function for extracting text
def get_text(save_dir, file_name, write_=False):
    read_dir = os.path.normpath(os.path.join(save_dir, file_name))
    img = preprocess_image(read_dir)
    
    if img is None:
        print(f"Error: Unable to read image file {read_dir}")
        return {}

    contours, hierarchy, img = ignore_lines(img, save_dir, file_name)
    contoursBBS = make_rows(contours)
    merge_cnt = merge_boxes(img, contoursBBS, thresh_x=1.0, thresh_y=0.6)
    column_contours = segment_columns(img, img.shape, merge_cnt)

    key_nodes = []
    text_val = {}
    node_number = 0

    for cnt in sorted(merge_cnt):
        for contour in merge_cnt[cnt]:
            node_number += 1
            [x, y, w, h] = contour
            if h < 10:
                continue
            cropped = img[max(0, y-2): y + h + 2, max(0, x - 2): x + w + 2]

            text = pytesseract.image_to_string(cropped, lang='eng', config='--psm 6')
            for tex in text.split():
                tex = tex.lower()
                if tex in labels:
                    key_nodes.append(node_number - 1)
                    break
                else:
                    for k in labels:
                        if k in tex or (len(tex) >= 1 and levenshtein_ratio_and_distance(k, tex, ratio_calc=True) > 0.8):
                            key_nodes.append(node_number - 1)
                            break
            text_val[node_number - 1] = text

    return text_val

# Dummy extract_key_value_pairs function
def extract_key_value_pairs(text_data, synonyms):
    # Placeholder for the actual extraction logic
    extracted_data = {field: 'No data found' for field in expected_fields}
    return extracted_data

# Main function
def main(image_path, save_dir, write_=False):
    image_path = os.path.normpath(image_path)
    save_dir = os.path.normpath(save_dir)
    
    text_data = get_text(save_dir, os.path.basename(image_path), write_=write_)
    extracted_data = extract_key_value_pairs(text_data, synonyms)
    
    csv_file_path = os.path.normpath(os.path.join(save_dir, 'extracted_data.csv'))
    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Field', 'Data', 'Confidence'])

        for label, value in extracted_data.items():
            confidence = "95.00%" if value != 'No data found' else "0.00%"
            csv_writer.writerow([label, value, confidence])
            print(f"Writing to CSV: {label}, {value}, {confidence}")

if __name__ == '__main__':
    image_path = r"C:\\Users\\jyoti\\Desktop\\imgs\\10_page_1.jpg"
    save_dir = r"C:\\Users\\jyoti\\Desktop\\csvs"
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    main(image_path, save_dir)

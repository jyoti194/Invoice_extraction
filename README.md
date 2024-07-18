# Invoice_extraction

## Project Overview
This project extracts specific fields from PDF or image files of invoices using Optical Character Recognition (OCR) and saves the extracted data into a CSV file. The extraction process includes preprocessing images, applying OCR to extract text, identifying relevant fields, and saving the results with confidence scores.

## Table of Contents
*  Installation
* Usage
* Structure
* Configuration
* Explanation of Code
* Installation
## Prerequisites
* Python 3.6+
* Tesseract OCR
* Required Python libraries
## Steps
* Install Tesseract OCR:

Install Python Dependencies:
* pip install -r requirements.txt
* Python Libraries
The required libraries are listed in requirements.txt:
* opencv-python
* pytesseract
* pandas
* numpy
  
# Usage
## Directory Setup
* Place your image files in a directory (e.g., input_images).
* Create an output directory to store the CSV files (e.g., output_csvs).

## Running the Script
Edit the Configuration:

Update the image_dir and output_dir variables in the script to point to your directories.

# Configuration
## Script Parameters
* image_dir: Directory containing input image files.
* output_dir: Directory to save the output CSV files.
* Fields and Patterns
The script uses predefined patterns and labels for extracting specific fields from the invoices. You can modify these patterns in the script to match your invoice formats.

## Confidence Scores
The script retrieves confidence scores from the OCR output for each extracted field. If a field is not found, the confidence score is set to 0.

# Explanation of Code
extract_text.py
## Preprocessing:

Converts images to grayscale.
Applies adaptive thresholding for better OCR results.
Text Extraction:

Uses Tesseract OCR to extract text from images.
Field Matching:

Uses regular expressions or label matching to identify relevant fields in the extracted text.
Output:

Saves extracted data and confidence scores to a CSV file.
merge_boxes.py and rem_lines.py
These utility scripts handle image segmentation and line removal to improve OCR accuracy.

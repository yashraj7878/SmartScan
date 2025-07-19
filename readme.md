# 📦 SmartScan: Image-Based Product Metadata Extraction with OCR + ML

## 🚀 Project Overview

**SmartScan** is a hybrid OCR + Machine Learning solution designed to extract structured metadata (like weight, volume, and dimensions) directly from product images. This approach is essential in domains like e-commerce and healthcare, where detailed product specs are critical, but often missing or embedded only in visuals.

The system leverages deep learning-based computer vision models and OCR to detect and extract textual entities such as:

- Weight (e.g., `800.00 gram`)
- Volume
- Voltage
- Wattage
- Dimensions (height, width, depth)

The final outputs are formatted predictions suitable for cataloging, moderation, or automation tasks.

## 📂 Dataset Description

The dataset comprises the following fields:

- **index**: Unique identifier for each image sample  
- **image_link**: Public URL of the product image  
- **group_id**: Category ID for the product  
- **entity_name**: The target metadata entity (e.g., `item_weight`, `height`, `voltage`)  
- **entity_value**: The actual value to extract (e.g., `800 gram`) – *only present in training data*

> In the test data, `entity_value` is omitted. The model is expected to predict this value from the image and `entity_name`.

## 🛠️ Solution Approach

### 🔍 1. **OCR-Based Feature Extraction**
- Used **EasyOCR** to extract textual information embedded in product images.
- Parsed outputs to locate key numerical-entity patterns.

### 🧠 2. **CNN Feature Modeling**
- Applied **ResNet18** to extract image features that encode visual clues for entity prediction.
- Combined OCR text and CNN image embeddings for higher accuracy.

### ⚙️ 3. **ML Pipeline**
- Post-processed predictions to ensure formatting constraints:
  - Standard float representation (e.g., `3.50`, not `3.5e0`)
  - Units strictly from the allowed list
- Filtered and normalized outputs to ensure quality and compliance.


## 💻 Technologies Used

- **Machine Learning**
- **Computer Vision**
- **Deep Learning** (ResNet18)
- **OCR** (EasyOCR)
- **Python**, **NumPy**, **Pandas**, **OpenCV**
- **Image Preprocessing** & **Text Post-Processing**

## ✅ Highlights

- 🚀 Hybrid OCR + Deep Learning pipeline  
- 🔢 Structured extraction of 8+ product metadata types  
- ✅ Sanity-checked, format-compliant predictions  
- 📊 85%+ F1 score on validation set  



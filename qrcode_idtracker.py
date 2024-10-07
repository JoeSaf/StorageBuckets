import os
import json
import random
import qrcode
from PIL import Image, ImageTk

# Define directories
UPLOAD_DIR = "upload"
QR_CODE_DIR = os.path.join(UPLOAD_DIR, "qr_codes")

# Ensure the QR code directory exists
if not os.path.exists(QR_CODE_DIR):
    os.makedirs(QR_CODE_DIR)

def generate_qr_code(file_path):
    # Check if the QR code already exists for the file
    existing_qr_image = check_existing_qr_code(file_path)
    if existing_qr_image:
        print(f"QR Code already exists at: {existing_qr_image}")
        # Load and return the existing QR code image
        qr_img = Image.open(existing_qr_image)
        qr_img_resized = qr_img.resize((150, 150), Image.LANCZOS)
        qr_tk = ImageTk.PhotoImage(qr_img_resized)
        return qr_tk  # Return the existing QR code image to display

    # Generate a new unique_id for the new QR code
    unique_id = random.randint(100000, 999999)

    # Create a new QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(file_path)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    # Save the new QR code to an image in the QR_CODE_DIR
    img_path = os.path.join(QR_CODE_DIR, f"qr_code_{unique_id}.png")
    img.save(img_path)

    # Save the unique_id and file path to a JSON file
    save_upload_record(unique_id, file_path)

    # Display the new QR code
    qr_img = Image.open(img_path)
    qr_img_resized = qr_img.resize((150, 150), Image.LANCZOS)
    qr_tk = ImageTk.PhotoImage(qr_img_resized)

    return qr_tk  # Return the new QR code image to display

def check_existing_qr_code(file_path):
    """
    Check if a QR code has already been created for the given file.
    Returns the path to the existing QR code image if found, else None.
    """
    # Load existing records
    records = load_existing_records()
    
    # Check if the file_path exists in the records
    for record in records:
        if record['file_path'] == file_path:
            # Build the path for the existing QR code image
            existing_qr_image = os.path.join(QR_CODE_DIR, f"qr_code_{record['id']}.png")
            if os.path.exists(existing_qr_image):
                return existing_qr_image

    return None

def save_upload_record(unique_id, file_path):
    """
    Saves the upload record to a JSON file.
    """
    record = {
        "id": unique_id,
        "file_path": file_path
    }

    # Load existing records
    records = load_existing_records()

    # Append new record
    records.append(record)

    # Save updated records
    with open("upload_records.json", "w") as f:
        json.dump(records, f, indent=4)

def load_existing_records():
    """
    Loads existing upload records from the JSON file.
    """
    if os.path.exists("upload_records.json"):
        with open("upload_records.json", "r") as f:
            return json.load(f)
    return []

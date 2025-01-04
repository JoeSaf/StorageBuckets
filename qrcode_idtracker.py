import os
import json
import random
import hashlib
import qrcode
from PIL import Image, ImageTk

# Define directories
UPLOAD_DIR = "upload"
QR_CODE_DIR = os.path.join(UPLOAD_DIR, "qr_codes")

# Ensure the QR code directory exists
if not os.path.exists(QR_CODE_DIR):
    os.makedirs(QR_CODE_DIR)

def get_file_hash(file_path):
    """
    Generate a SHA-256 hash of a file to track uniqueness.
    """
    try:
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None

def generate_qr_code(file_path):
    """
    Generates a QR code for the given file.
    If a QR code already exists for this file (based on its hash), it is reused.
    """
    file_hash = get_file_hash(file_path)
    if not file_hash:
        print(f"Error: File not found -> {file_path}")
        return None

    # Check if a QR code already exists for this file
    existing_qr_image = check_existing_qr_code(file_hash)
    if existing_qr_image:
        qr_img = Image.open(existing_qr_image)
        qr_img_resized = qr_img.resize((150, 150), Image.LANCZOS)
        return ImageTk.PhotoImage(qr_img_resized)

    # Generate a new unique ID for the QR code
    unique_id = random.randint(100000, 999999)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(file_path)  # Keep the file path but track the hash
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    # Save the QR code image
    img_path = os.path.join(QR_CODE_DIR, f"qr_code_{unique_id}.png")
    img.save(img_path)

    # Save upload record with file hash
    save_upload_record(unique_id, file_hash, file_path)

    qr_img = Image.open(img_path)
    qr_img_resized = qr_img.resize((150, 150), Image.LANCZOS)
    return ImageTk.PhotoImage(qr_img_resized)

def check_existing_qr_code(file_hash):
    """
    Checks if a QR code has already been created for the given file hash.
    Returns the path to the existing QR code image if found, else None.
    """
    records = load_existing_records()
    for record in records:
        if record['file_hash'] == file_hash:
            existing_qr_image = os.path.join(QR_CODE_DIR, f"qr_code_{record['id']}.png")
            if os.path.exists(existing_qr_image):
                return existing_qr_image
    return None

def save_upload_record(unique_id, file_hash, file_path):
    """
    Saves the upload record to a JSON file.
    """
    record = {
        "id": unique_id,
        "file_hash": file_hash,
        "file_path": file_path
    }

    records = load_existing_records()
    records.append(record)

    with open("upload_records.json", "w") as f:
        json.dump(records, f, indent=4)

def load_existing_records():
    """
    Loads existing upload records from the JSON file.
    If the file is missing or invalid, it returns an empty list.
    """
    try:
        if os.path.exists("upload_records.json"):
            with open("upload_records.json", "r") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Warning: Could not load upload records. Resetting.")
        return []
    return []

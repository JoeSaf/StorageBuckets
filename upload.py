import os
import json
from datetime import datetime
from tkinter import filedialog, Tk, messagebox, simpledialog

# Global variables
UPLOAD_DIR = "upload"
UPLOAD_LOG = "upload_log.json"
BUCKET_DIR = "buckets"  # Directory to hold all bucket directories

def create_upload_directory():
    """
    Creates an 'upload/' directory if it doesn't exist.
    """
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
        print(f"Directory '{UPLOAD_DIR}' created successfully.")
    else:
        print(f"Directory '{UPLOAD_DIR}' already exists.")

def record_upload(file_name, destination):
    """
    Records the details of each upload in a JSON log file.
    """
    # Create a dictionary entry for the file
    upload_record = {
        "file_name": file_name,
        "destination": destination,
        "upload_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Load existing log or create a new one
    if os.path.exists(UPLOAD_LOG):
        with open(UPLOAD_LOG, 'r') as log_file:
            upload_data = json.load(log_file)
    else:
        upload_data = []

    # Append new upload record and save back to file
    upload_data.append(upload_record)

    with open(UPLOAD_LOG, 'w') as log_file:
        json.dump(upload_data, log_file, indent=4)
    
    print(f"Recorded upload: {file_name} to {destination}")

def select_bucket():
    """
    Prompts the user to select a bucket from the available buckets.
    Returns the path of the selected bucket or None if no bucket is selected.
    """
    if not os.path.exists(BUCKET_DIR):
        return None  # No buckets exist

    # List all buckets
    buckets = [name for name in os.listdir(BUCKET_DIR) if os.path.isdir(os.path.join(BUCKET_DIR, name))]
    
    if not buckets:
        return None  # No buckets available

    # Prompt user to select a bucket
    bucket_choice = simpledialog.askstring("Select Bucket", "Available buckets:\n" + "\n".join(buckets) + "\n\nType the bucket name or leave blank to upload to the default directory:")
    
    if bucket_choice in buckets:
        return os.path.join(BUCKET_DIR, bucket_choice)
    return None  # User chose not to select a bucket

def upload_files():
    """
    Function to upload multiple files using a file dialog.
    """
    # Tkinter root hidden window (to open dialog without full GUI)
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    
    # Ask user to select multiple files
    files = filedialog.askopenfilenames(title="Select files to upload")

    if not files:
        messagebox.showinfo("No file selected", "No files were selected for upload.")
        return

    create_upload_directory()  # Ensure upload directory exists
    
    # Allow user to select a bucket or default to upload/
    selected_bucket = select_bucket()
    upload_location = selected_bucket if selected_bucket else UPLOAD_DIR

    # Process each file
    for file_path in files:
        try:
            # Get file name
            file_name = os.path.basename(file_path)
            # Destination path in the chosen bucket or upload/ directory
            dest_path = os.path.join(upload_location, file_name)
            
            # Create the bucket directory if it doesn't exist
            if selected_bucket and not os.path.exists(selected_bucket):
                os.makedirs(selected_bucket)

            # Copy file to the chosen location
            with open(file_path, 'rb') as src_file:
                with open(dest_path, 'wb') as dest_file:
                    dest_file.write(src_file.read())

            print(f"Uploaded {file_name} to {upload_location}")
            record_upload(file_name, upload_location)  # Record the upload in JSON

        except Exception as e:
            print(f"Failed to upload {file_name}: {e}")

    messagebox.showinfo("Upload Complete", "All files have been uploaded successfully.")

if __name__ == "__main__":
    upload_files()

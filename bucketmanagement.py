import os
import qrcode_idtracker  # Import the QR code tracker module
import shutil
from tkinter import simpledialog, messagebox

# Directories for storing buckets and uploads
BUCKET_DIR = "buckets"
UPLOADS_DIR = "upload"

def ensure_bucket_directory():
    """Ensures the bucket directory exists."""
    if not os.path.exists(BUCKET_DIR):
        os.makedirs(BUCKET_DIR)

def ensure_uploads_directory():
    """Ensures the uploads directory exists."""
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)

def create_bucket():
    """Prompts the user for a bucket name and creates a directory."""
    ensure_bucket_directory()
    bucket_name = simpledialog.askstring("Input", "Enter bucket name:")
    
    if bucket_name:
        bucket_path = os.path.join(BUCKET_DIR, bucket_name)
        if not os.path.exists(bucket_path):
            os.makedirs(bucket_path)
            messagebox.showinfo("Success", f"Bucket '{bucket_name}' created successfully.")
        else:
            messagebox.showerror("Error", f"Bucket '{bucket_name}' already exists.")
    else:
        messagebox.showwarning("Input Error", "Bucket name cannot be empty.")

def delete_bucket():
    """Prompts the user to select a bucket and deletes it."""
    ensure_bucket_directory()
    buckets = os.listdir(BUCKET_DIR)
    
    if not buckets:
        messagebox.showwarning("Error", "No buckets available to delete.")
        return
    
    bucket_to_delete = simpledialog.askstring("Delete Bucket", f"Available buckets: {', '.join(buckets)}\nEnter bucket name to delete:")
    
    if bucket_to_delete and bucket_to_delete in buckets:
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the bucket '{bucket_to_delete}' and all its contents?")
        if confirm:
            bucket_path = os.path.join(BUCKET_DIR, bucket_to_delete)
            try:
                shutil.rmtree(bucket_path)
                messagebox.showinfo("Success", f"Bucket '{bucket_to_delete}' deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete bucket '{bucket_to_delete}': {e}")
    else:
        messagebox.showwarning("Error", "Invalid bucket name selected.")

def download_file_from_bucket(bucket_name, file_name, destination_dir):
    """Downloads a file from a bucket or the uploads directory to the specified destination."""
    ensure_bucket_directory()
    ensure_uploads_directory()

    file_path = os.path.join(BUCKET_DIR, bucket_name, file_name) if bucket_name != "Uploads" else os.path.join(UPLOADS_DIR, file_name)

    if not os.path.exists(file_path):
        messagebox.showerror("Error", f"File '{file_name}' does not exist in '{bucket_name}'.")
        return

    destination = os.path.join(destination_dir, "storageBucketDownloads")
    if not os.path.exists(destination):
        os.makedirs(destination)

    destination_file_path = os.path.join(destination, file_name)
    
    if os.path.exists(destination_file_path):
        messagebox.showwarning("Warning", f"File '{file_name}' already exists in '{destination}'. Skipping.")
        return

    try:
        shutil.copy(file_path, destination_file_path)
        messagebox.showinfo("Success", f"File '{file_name}' downloaded to '{destination}'.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not download file: {e}")

def download_selected_files(tree):
    """Downloads selected files from a bucket or uploads directory."""
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showerror("Error", "No files selected. Please select files to download.")
        return

    files_to_download = []
    bucket_name = None

    for item in selected_items:
        parent_item = tree.parent(item)
        item_name = tree.item(item, 'text')

        if parent_item:  
            bucket_name = tree.item(parent_item, 'text')  # Parent is the bucket name
            files_to_download.append(item_name)
        elif item_name in os.listdir(UPLOADS_DIR):
            bucket_name = "Uploads"
            files_to_download.append(item_name)
        else:
            messagebox.showerror("Error", f"Invalid selection: {item_name} is not a file.")
            return

    if not files_to_download:
        messagebox.showwarning("Error", "No valid files selected for download.")
        return

    destination = simpledialog.askstring("Download", "Enter the destination path to save the files:")
    if not destination:
        messagebox.showwarning("Input Error", "Download path cannot be empty.")
        return

    for file_name in files_to_download:
        print(f"Downloading file: {file_name} from '{bucket_name}'")
        download_file_from_bucket(bucket_name, file_name, destination)

    messagebox.showinfo("Download Status", f"Downloaded {len(files_to_download)} file(s) from '{bucket_name}'.")

import os
import qrcode_idtracker  # Import the new QR code tracker
import shutil
from tkinter import simpledialog, messagebox

# Directory where buckets and uploads will be stored
BUCKET_DIR = "buckets"
UPLOADS_DIR = "upload"

def ensure_bucket_directory():
    """
    Ensures that the bucket directory exists. If it doesn't exist, it creates it.
    """
    if not os.path.exists(BUCKET_DIR):
        os.makedirs(BUCKET_DIR)

def ensure_uploads_directory():
    """
    Ensures that the uploads directory exists. If it doesn't exist, it creates it.
    """
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)

def create_bucket():
    """
    Prompts the user for a bucket name and creates a directory with that name.
    """
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
    """
    Prompts the user to select a bucket and deletes the corresponding directory.
    """
    ensure_bucket_directory()
    buckets = os.listdir(BUCKET_DIR)
    
    if not buckets:
        messagebox.showwarning("Error", "No buckets available to delete.")
        return
    
    # Prompting the user to choose a bucket to delete
    bucket_to_delete = simpledialog.askstring("Delete Bucket", f"Available buckets: {', '.join(buckets)}\nEnter bucket name to delete:")
    
    if bucket_to_delete in buckets:
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the bucket '{bucket_to_delete}' and all its contents?")
        if confirm:
            bucket_path = os.path.join(BUCKET_DIR, bucket_to_delete)
            try:
                shutil.rmtree(bucket_path)  # Remove non-empty directory
                messagebox.showinfo("Success", f"Bucket '{bucket_to_delete}' deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete bucket '{bucket_to_delete}': {e}")
        else:
            messagebox.showinfo("Cancelled", f"Deletion of bucket '{bucket_to_delete}' was cancelled.")
    else:
        messagebox.showwarning("Error", "Invalid bucket name selected.")

def download_file_from_bucket(bucket_name, file_name, destination_dir):
    """
    Downloads a file from the specified bucket or uploads directory to the given destination directory.
    """
    # Check in the specified bucket
    bucket_path = os.path.join(BUCKET_DIR, bucket_name)
    file_path = os.path.join(bucket_path, file_name)

    # If not found in bucket, check in uploads directory
    if not os.path.exists(file_path):
        file_path = os.path.join(UPLOADS_DIR, file_name)

    if not os.path.exists(file_path):
        messagebox.showerror("Error", f"File '{file_name}' does not exist in bucket '{bucket_name}' or uploads.")
        return

    destination = os.path.join(destination_dir, "storageBucketDownloads")  # Create destination directory
    if not os.path.exists(destination):
        os.makedirs(destination)  # Create the folder if it doesn't exist

    destination_file_path = os.path.join(destination, file_name)
    try:
        shutil.copy(file_path, destination_file_path)
        messagebox.showinfo("Success", f"File '{file_name}' downloaded to '{destination}'.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not download file: {e}")

def download_selected_files(tree):
    """
    Downloads selected files from the specified bucket or uploads directory to a user-defined location.
    """
    selected_items = tree.selection()
    if selected_items:
        files_to_download = []
        bucket_name = None
        
        for item in selected_items:
            # Get the parent to check if it's a bucket or uploads
            parent_item = tree.parent(item)
            item_name = tree.item(item, 'text')

            if parent_item:
                # Get the bucket name if it's a file under a bucket
                bucket_name = tree.item(parent_item, 'text')
                files_to_download.append(item_name)
            else:
                # Check if the item is from uploads
                if item_name == "Uploads":  # Assuming "Uploads" is the name of the uploads folder in the tree
                    bucket_name = "Uploads"
                    files_to_download.append(item_name)  # Add the file name here
                else:
                    messagebox.showerror("Error", "Please select files from a bucket or uploads to download.")
                    return

        # If we have collected files to download
        if bucket_name:
            destination = simpledialog.askstring("Download", "Enter the destination path to save the files:")
            if destination:  # Ensure the destination is provided
                for file_name in files_to_download:
                    print(f"Downloading file: {file_name} from bucket: {bucket_name}")
                    download_file_from_bucket(bucket_name, file_name, destination)  # Pass the download directory
                messagebox.showinfo("Download Status", f"Downloaded {len(files_to_download)} file(s) from '{bucket_name}'.")
    else:
        messagebox.showerror("Error", "No files selected. Please select files to download.")


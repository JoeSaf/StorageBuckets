import os
from tkinter import simpledialog, messagebox

# Directory where buckets will be stored (representing the "buckets")
BUCKET_DIR = "buckets"

def ensure_bucket_directory():
    """
    Ensures that the bucket directory exists. If it doesn't exist, it creates it.
    """
    if not os.path.exists(BUCKET_DIR):
        os.makedirs(BUCKET_DIR)

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
        bucket_path = os.path.join(BUCKET_DIR, bucket_to_delete)
        try:
            os.rmdir(bucket_path)  # This will only remove empty directories
            messagebox.showinfo("Success", f"Bucket '{bucket_to_delete}' deleted successfully.")
        except OSError:
            messagebox.showerror("Error", f"Bucket '{bucket_to_delete}' is not empty or cannot be deleted.")
    else:
        messagebox.showwarning("Error", "Invalid bucket name selected.")

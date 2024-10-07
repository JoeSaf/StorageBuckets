import tkinter as tk
from tkinter import ttk, messagebox
import os
import qrcode_idtracker  # Import the new QR code tracker
from PIL import Image, ImageTk
from upload import upload_files
from bucketmanagement import create_bucket, delete_bucket

# directories where the uploaded files and buckets are stored
UPLOAD_DIR = "upload/"  # here normal uploads are placed
BUCKET_DIR = "buckets/"  # here privatized uploads are kept in their buckets

def toggle_qr_code():
    selected_item = tree.selection()
    if selected_item:
        file_name = tree.item(selected_item, 'text')
        file_path = os.path.join(UPLOAD_DIR, file_name)  # Corrected file path to check in UPLOAD_DIR
        
        print(f"Selected file: {file_name}")
        print(f"Generating QR code for file path: {file_path}")

        # Generate QR code
        qr_image = qrcode_idtracker.generate_qr_code(file_path)
        
        # Check if qr_image is valid
        if qr_image:
            print("QR code generated successfully.")
            qr_label.config(image=qr_image)
            qr_label.image = qr_image  # Keep a reference to avoid garbage collection
        else:
            print("Failed to generate QR code.")
            messagebox.showerror("Error", "Could not generate QR code.")
    else:
        print("No file selected.")
        qr_label.config(image='', text="QR Code display is disabled.")  # Clear the QR label if nothing is selected

# A function for tree view
def populate_tree():
    # Clear the tree view
    for item in tree.get_children():
        tree.delete(item)

    # Insert root nodes for uploads and buckets
    uploads_node = tree.insert('', 'end', text="Uploads", open=True)
    buckets_node = tree.insert('', 'end', text="Buckets", open=True)

    # Uploads
    if os.path.exists(UPLOAD_DIR):
        for file_name in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, file_name)
            if os.path.isfile(file_path):
                tree.insert(uploads_node, 'end', text=file_name)

    # Buckets
    if os.path.exists(BUCKET_DIR):
        for bucket_name in os.listdir(BUCKET_DIR):
            bucket_path = os.path.join(BUCKET_DIR, bucket_name)
            if os.path.isdir(bucket_path):
                bucket_node = tree.insert(buckets_node, 'end', text=bucket_name)

                # Files in the bucket
                for file_name in os.listdir(bucket_path):
                    file_path = os.path.join(bucket_path, file_name)
                    if os.path.isfile(file_path):
                        tree.insert(bucket_node, 'end', text=file_name)

def initiate_upload():
    upload_files()  # Upload function
    populate_tree()  # Refresh function
    messagebox.showinfo("Upload Status", "File upload process completed.")

def open_create_bucket():
    create_bucket()  # Bucket creation function
    populate_tree()  # Refresh function

def open_delete_bucket():
    delete_bucket()  # Allows user to delete bucket
    populate_tree()  # Refresh the tree

# Main window
root = tk.Tk()
root.title("Storage Bucket")
root.geometry("800x600")

# Frame for file structure and search box (left side)
left_frame = tk.Frame(root, width=400)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Search box
search_label = tk.Label(left_frame, text="Enter search term:")
search_label.pack(anchor="w")
search_entry = tk.Entry(left_frame, width=40)
search_entry.pack(anchor="w", pady=5)

# Treeview for folder structure
tree = ttk.Treeview(left_frame)
tree.pack(expand=True, fill=tk.BOTH)

# Frame for menu and settings (right side)
right_frame = tk.Frame(root, width=300)
right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# Menu buttons (Upload, Bucket Management, Settings)
upload_button = tk.Button(right_frame, text="Upload File(s)", command=initiate_upload)
upload_button.pack(pady=10)

create_bucket_button = tk.Button(right_frame, text="Create Bucket", command=open_create_bucket)
create_bucket_button.pack(pady=10)

delete_bucket_button = tk.Button(right_frame, text="Delete Bucket", command=open_delete_bucket)
delete_bucket_button.pack(pady=10)

settings_button = tk.Button(right_frame, text="Settings")
settings_button.pack(pady=10)

# Checkbox for showing QR Code
qr_var = tk.BooleanVar()
qr_var.set(False)
qr_checkbox = tk.Checkbutton(right_frame, text="Show QR Code for selected file", variable=qr_var, command=toggle_qr_code)
qr_checkbox.pack(pady=20)

# QR Code display area
qr_label = tk.Label(right_frame, text="QR Code display is disabled.", width=40, height=10, bg="lightgrey", relief=tk.SUNKEN)
qr_label.pack(pady=10)

# Populate the treeview with file structure and buckets
populate_tree()

# Start the Tkinter event loop
root.mainloop()

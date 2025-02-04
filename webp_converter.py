import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import os

def convert_to_webp(images, quality, output_folder):
    for image_path in images:
        output_path = os.path.splitext(image_path)[0] + '.webp'
        if output_folder:
            output_path = os.path.join(output_folder, os.path.basename(output_path))
        subprocess.run(['cwebp', '-q', str(quality), image_path, '-o', output_path])
        print(f"Converted {image_path} to {output_path}")

def select_files():
    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    if file_paths:
        file_listbox.delete(0, tk.END)
        for file_path in file_paths:
            file_listbox.insert(tk.END, file_path)

def select_output_folder():
    folder_path = filedialog.askdirectory(title="Select Output Folder")
    if folder_path:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, folder_path)

def convert_images():
    quality = quality_slider.get()
    images = file_listbox.get(0, tk.END)
    output_folder = output_folder_entry.get()
    if images:
        convert_to_webp(images, quality, output_folder)
        messagebox.showinfo("Success", "Images converted successfully!")
    else:
        messagebox.showwarning("No Images Selected", "Please select images to convert.")

def update_quality_from_entry(event):
    try:
        quality = int(quality_entry.get())
        if 0 <= quality <= 100:
            quality_slider.set(quality)
        else:
            messagebox.showwarning("Invalid Quality", "Please enter a value between 0 and 100.")
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a valid integer.")

def update_quality_from_slider(val):
    quality_entry.delete(0, tk.END)
    quality_entry.insert(0, val)

# Set up the main window
root = tk.Tk()
root.title("Image to WebP Converter")

# Create and pack the widgets
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

select_button = tk.Button(frame, text="Select Images", command=select_files)
select_button.pack(pady=5)

file_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=50)
file_listbox.pack(pady=5)

quality_label = tk.Label(frame, text="Quality:")
quality_label.pack(pady=5)

quality_slider = tk.Scale(frame, from_=0, to_=100, orient=tk.HORIZONTAL, command=update_quality_from_slider)
quality_slider.set(75)  # default value
quality_slider.pack(pady=5)

quality_entry = tk.Entry(frame, width=5)
quality_entry.insert(0, "75")
quality_entry.bind("<Return>", update_quality_from_entry)
quality_entry.pack(pady=5)

output_folder_label = tk.Label(frame, text="Output Folder (optional):")
output_folder_label.pack(pady=5)

output_folder_entry = tk.Entry(frame, width=50)
output_folder_entry.pack(pady=5)

select_output_button = tk.Button(frame, text="Select Output Folder", command=select_output_folder)
select_output_button.pack(pady=5)

convert_button = tk.Button(frame, text="Convert to WebP", command=convert_images)
convert_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()

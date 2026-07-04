import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import json
import os

DATABASE = "hashes.json"

# Create database if it doesn't exist
if not os.path.exists(DATABASE):
    with open(DATABASE, "w") as f:
        json.dump({}, f)


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()


def save_hash():
    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    file_hash = calculate_hash(file_path)

    with open(DATABASE, "r") as f:
        data = json.load(f)

    data[file_path] = file_hash

    with open(DATABASE, "w") as f:
        json.dump(data, f, indent=4)

    messagebox.showinfo(
        "Success",
        "File hash saved successfully!"
    )


def verify_hash():
    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    with open(DATABASE, "r") as f:
        data = json.load(f)

    if file_path not in data:
        messagebox.showerror(
            "Error",
            "No saved hash found for this file."
        )
        return

    current_hash = calculate_hash(file_path)

    if current_hash == data[file_path]:
        messagebox.showinfo(
            "Verification",
            "✅ File Integrity Verified.\nFile has NOT been modified."
        )
    else:
        messagebox.showwarning(
            "Verification",
            "❌ WARNING!\nFile has been modified."
        )


def show_saved_files():
    with open(DATABASE, "r") as f:
        data = json.load(f)

    if not data:
        messagebox.showinfo(
            "Saved Files",
            "No files stored."
        )
        return

    text = ""

    for file in data:
        text += file + "\n\n"

    messagebox.showinfo(
        "Saved Files",
        text
    )


root = tk.Tk()

root.title("Cyber Security - File Integrity Checker")
root.geometry("500x350")

title = tk.Label(
    root,
    text="File Integrity Checker",
    font=("Arial", 18, "bold")
)

title.pack(pady=20)

btn1 = tk.Button(
    root,
    text="Save File Hash",
    width=25,
    command=save_hash
)

btn1.pack(pady=10)

btn2 = tk.Button(
    root,
    text="Verify File",
    width=25,
    command=verify_hash
)

btn2.pack(pady=10)

btn3 = tk.Button(
    root,
    text="Show Saved Files",
    width=25,
    command=show_saved_files
)

btn3.pack(pady=10)

btn4 = tk.Button(
    root,
    text="Exit",
    width=25,
    command=root.destroy
)

btn4.pack(pady=10)

root.mainloop()
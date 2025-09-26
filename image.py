import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

def process_image(image_path, key, mode="encrypt"):
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
    width, height = img.size

    if mode == "encrypt":
        # Add key to each pixel value
        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                pixels[x, y] = ((r + key) % 256, (g + key) % 256, (b + key) % 256)

        # Horizontal flip
        for y in range(height):
            for x in range(width // 2):
                pixels[x, y], pixels[width - x - 1, y] = pixels[width - x - 1, y], pixels[x, y]
    else:
        # Reverse horizontal flip
        for y in range(height):
            for x in range(width // 2):
                pixels[x, y], pixels[width - x - 1, y] = pixels[width - x - 1, y], pixels[x, y]

        # Subtract key
        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                pixels[x, y] = ((r - key) % 256, (g - key) % 256, (b - key) % 256)

    return img

class ImageEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Image Encryptor")

        self.original_image = None
        self.processed_image = None
        self.image_path = None

        # Widgets
        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.key_label = tk.Label(root, text="Key:")
        self.key_label.pack()

        self.key_entry = tk.Entry(root)
        self.key_entry.insert(0, "50")
        self.key_entry.pack()

        self.encrypt_button = tk.Button(root, text="Encrypt", command=self.encrypt_image)
        self.encrypt_button.pack()

        self.decrypt_button = tk.Button(root, text="Decrypt", command=self.decrypt_image)
        self.decrypt_button.pack()

        self.save_button = tk.Button(root, text="Save Processed Image", command=self.save_image)
        self.save_button.pack()

        self.canvas = tk.Canvas(root, width=800, height=400)
        self.canvas.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.bmp *.jpeg")])
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.display_images()

    def display_images(self):
        self.canvas.delete("all")
        if self.original_image:
            img1 = self.original_image.resize((400, 400))
            self.tk_img1 = ImageTk.PhotoImage(img1)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img1)

        if self.processed_image:
            img2 = self.processed_image.resize((400, 400))
            self.tk_img2 = ImageTk.PhotoImage(img2)
            self.canvas.create_image(400, 0, anchor=tk.NW, image=self.tk_img2)

    def get_key(self):
        try:
            return int(self.key_entry.get()) % 256
        except ValueError:
            messagebox.showerror("Invalid Key", "Key must be an integer.")
            return None

    def encrypt_image(self):
        key = self.get_key()
        if self.image_path and key is not None:
            self.processed_image = process_image(self.image_path, key, mode="encrypt")
            self.display_images()

    def decrypt_image(self):
        key = self.get_key()
        if self.image_path and key is not None:
            self.processed_image = process_image(self.image_path, key, mode="decrypt")
            self.display_images()

    def save_image(self):
        if self.processed_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("Bitmap files", "*.bmp")])
            if save_path:
                self.processed_image.save(save_path)
                messagebox.showinfo("Image Saved", f"Image saved to {save_path}")
        else:
            messagebox.showwarning("No Image", "No processed image to save.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorApp(root)
    root.mainloop()

import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.attributes("-fullscreen", True)

bg_label = tk.Label(root)
bg_label.place(relwidth=1, relheight=1)

def update_background(bg_path):
    try:
        width = root.winfo_width()
        height = root.winfo_height()
        image = Image.open(bg_path)
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)
        bg_label.config(image=bg_image)
        bg_label.image = bg_image
    except Exception as e:
        print(f"Error: {e}")

root.after(100, lambda: update_background("background_1.jpg"))
root.mainloop()

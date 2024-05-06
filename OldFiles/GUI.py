from tkinter import filedialog
from PIL import Image, ImageTk
# import DenseEncoding as de
import tkinter as tk

root = tk.Tk()
root.title("Simple GUI")
root.geometry("1280x720")


# root.resizable(width=False, height=False)

class custom_canvas(tk.Frame):
    def __init__(self, parent, width, height, background):
        self.canvas = tk.Canvas(parent, width=width, height=height, background=background)
        self.width = width
        self.height = height
        self.image = None


canvas1 = custom_canvas(root, 10000, 700, "Green")
canvas1.canvas.pack()


def resize_image_for_display(target_x, target_y, image):
    x, y = image.size
    change_x = target_x / x
    change_y = target_y / y
    if change_x < change_y:
        new_x = x * change_x
        new_y = y * change_x
    else:
        new_x = x * change_y
        new_y = y * change_y
    new_image = image.resize((int(new_x), int(new_y)))
    return new_image


def open_image(cust_canvas):
    canvas = cust_canvas.canvas
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    pil_image = Image.open(file_path)

    img = resize_image_for_display(cust_canvas.width, cust_canvas.height, pil_image)
    canvas.tk_image = ImageTk.PhotoImage(img)
    canvas.create_oval(0,0,100,100,fill="black")
    canvas.create_image((cust_canvas.width / 2, cust_canvas.height / 2), anchor="center", image=canvas.tk_image)
    canvas.update()
    canvas.configure(background="light blue")
    return pil_image

def button_open_image(cust_canvas):
    cust_canvas.image= open_image(cust_canvas)
    cust_canvas.image.show()


# def open_file():
#     file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png *.jpg *.jpeg")])
#
#     pil_image = tk.PhotoImage(file_path)  # Replace "example.jpg" with the path to your image file
#
#     canvas.create_image(0, 0, anchor=tk.NW, image=pil_image)


Button = tk.Button(root, height=100, width=100, text="Open", command=lambda: button_open_image(canvas1))
Button.pack()
# open_file()

root.mainloop()

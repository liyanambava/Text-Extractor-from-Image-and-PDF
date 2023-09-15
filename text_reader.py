import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import cv2
import pytesseract
import numpy as np
from PyPDF2 import PdfReader

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

root = tk.Tk()
root.title("Text Reader")

root.geometry("800x450")

heading = tk.Label(root, text = "Text Extractor", font=("Times New Roman", 25))
heading.pack(pady=40, anchor = 'n')

instruction = tk.Label(root, text = "Choose the picture you want to scan:", font=("Times New Roman", 18))
instruction.place(x = 400,  y = 120, anchor = 'center')

def file_select():
    global selected_file
    path = filedialog.askopenfilename(title="Select the File", filetypes=[("All files", "*.*"), ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"), ("PDF files", "*.pdf")])
    if path:
        selected_file = path
        file_path.config(text = f"{selected_file} has been selected", font=("Times New Roman",10), fg = "green")

def file_rem():
    global selected_file
    if selected_file:
        file_path.config(text = f"{selected_file} has been removed", font=("Times New Roman",10), fg = "red")
        selected_file = None

choose_file = tk.Button(root, text="Choose File", command=file_select)
choose_file.place(x = 250, y = 180)

remove_file = tk.Button(root, text="Remove File", command=file_rem)
remove_file.place(x = 450, y = 180)

file_path = tk.Label(root, text = "")
file_path.place(x = 210, y = 220)

def generate_text():
    global selected_file
    if selected_file:
        if selected_file.lower().endswith(('.pdf')):
            pdf_reader = PdfReader(open(selected_file, "rb"))
            text = ""
            for page in range(len(pdf_reader.pages)):
                p = pdf_reader.pages[page]
                text += p.extract_text()
        else:
            image = cv2.imread(selected_file)
            if image is not None:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                sharpened = cv2.filter2D(gray, -1, kernel)
                blur = cv2.GaussianBlur(sharpened, (5, 5), 0)
                median = cv2.medianBlur(blur, 3)
                threshold_image = cv2.threshold(median, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                img = threshold_image

                custom_config = r'--psm 6 --oem 3 -c tessedit_create_box=1 -c tessedit_write_images=1 -c tessedit_create_hocr=1 -l eng'
                text = pytesseract.image_to_string(img, lang = 'eng', config=custom_config)

        result.delete(1.0, tk.END)
        result.insert(tk.END, text)

generate = tk.Button(root, text = "Generate", command=generate_text)
generate.place(x = 395, y = 260, anchor = "center")

result = scrolledtext.ScrolledText(root, height=8, width=80)
result.place(x = 410, y = 349, anchor = "center")

root.mainloop()
import pytesseract
from back_end_code import image_processing
import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk

def add_to_the_list():
    if combobox_days.get() == 'better_contrast':
        a = entry1.get() 
        if a  not in [None,'',' ']:
            if 0 < float(a) <= 2:
                list_for_better_contrast.append(float(a))
            elif float(a) < 0:
                list_for_better_contrast.append(0.1)
            elif 2 < float(a):
                list_for_better_contrast.append(2)
        else:
            list_for_better_contrast.append(1)

    list_what_to_do.append(combobox_days.get())
    print_the_list_of_sraff()

def print_the_list_of_sraff():
    text_box_metods_OCR.delete("1.0", tk.END)
    cope_list = list_what_to_do.copy()
    text_box_metods_OCR.insert(tk.END, "\n".join([item for item in cope_list]))

def insert_change_the_image():
    try:
        new_image_path = return_the_file_plasment()
        
        if new_image_path:
            image_temp = Image.open(new_image_path)
            global image_format
            image_format = image_temp.format
            global image_cv2
            image_cv2 = cv2.imread(new_image_path)
            change_the_image_in_the_lable(image_cv2)
        else:
            print("No file selected.")
    except Exception as e:
        print("An error occurred:", e)

def change_the_image_in_the_lable(cv2_image):
    if cv2_image is None:
        print("Error loading image")
    else:
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        image_pil = Image.fromarray(image_rgb)

        # Check if PIL Image is created successfully
        if image_pil:
            # Create Tkinter-compatible image
            image_tk = ImageTk.PhotoImage(image_pil)

            # Update label with the new image
            lable_image.config(image=image_tk)

            # Keep a reference to the image to prevent garbage collection
            lable_image.image = image_tk
        else:
            print("Error converting image to PIL format")

def delet_by_index():
    numb = entry2.get()
    if 1 <= int(numb) <= len(list_what_to_do)-1:
        list_what_to_do.pop(int(numb))
    
def print_staff():
    print(list_what_to_do)

def return_the_file_plasment():
    filename = filedialog.askopenfilename()
    print("Selected file:", filename)
    return filename

def image_processing_for_buton():
    if image_cv2  is not None:
        new_image_to_text = image_processing(image_cv2,list_what_to_do,list_for_better_contrast.copy(),image_format)
        return new_image_to_text
    else:
        print('Dont have data to procese')
        print(image_cv2)

def image_to_text():
    post_image = image_processing_for_buton()
    if post_image is not None:
        text_val = pytesseract.image_to_string(post_image)
        print(text_val)
        # Clear existing text
        text_end_result.delete("1.0", tk.END)
        # Insert new text
        text_end_result.insert(tk.END, text_val)

def preshow_image_for_button():
    image = image_processing_for_buton()
    change_the_image_in_the_lable(image)

def to_the_txt_file_for_button():
    try:
        path_to_the_txt = return_the_file_plasment()
        if path_to_the_txt:
            post_image = image_processing_for_buton()
            with open(path_to_the_txt,'w') as file:
                text_val = pytesseract.image_to_string(post_image)
                for x in text_val:
                    file.write(x)
    except Exception as e:
        print('Fatal errer',e)

def insert_by_index_for_button():
    if combobox_days.get() not in ['',' ',None]:
        numb = entry2.get()
        numb = int(numb)
        if numb == len(list_what_to_do):
            list_what_to_do.append(combobox_days.get())
        elif 1 <= numb <= len(list_what_to_do)-1:
            list_what_to_do.insert(numb,combobox_days.get())
        print_the_list_of_sraff()

list_what_to_do = ['grayscale']
list_for_better_contrast = []
image_cv2 = None
image_format = ''

root = tk.Tk()
root.title("Project")

button_add_staff = tk.Button(root, text= 'Add to the format', command=add_to_the_list)
button_delte_staff = tk.Button(root, text= 'Delet by index',command= delet_by_index)
button_transtate_to_the_text = tk.Button(root, text= 'To the text', command= image_to_text)
button_upoad_the_image = tk.Button(root, text= 'Upload/Change image',command=insert_change_the_image)
button_preview_image = tk.Button(root, text= 'Preview image', command=preshow_image_for_button)
button_text_to_the_txt_file = tk.Button(root, text= 'To the txt file', command= to_the_txt_file_for_button)
button_for_insert_staff = tk.Button(root, text= 'Insert by index', command= insert_by_index_for_button)
temp_button = tk.Button(root, text= 'print',command= print_staff)

list_of_OCR = ["better_contrast","noise_removal","thin_fog","thick_fog","deskew","remove_bordesr","missing_border","invert_image","binarize"]
combobox_days = ttk.Combobox(root, values=list_of_OCR,state="readonly")

entry1 = tk.Entry(root, width=10)
entry2 = tk.Entry(root, width=10)

lable = tk.Label(root,text='<- starting form 1, 0 is constant')
lable_image = tk.Label(root,)

text_box_metods_OCR = tk.Text(root,width=30, height=10,)
text_end_result = tk.Text(root,width=30, height=10)

button_add_staff.grid(row=0, column=0, padx=10, pady=10)
combobox_days.grid(row=0, column=1, padx=10, pady=10)
entry1.grid(row=0, column=2, padx=10, pady=10)

button_delte_staff.grid(row=1, column=0, padx=10, pady=10)
button_for_insert_staff.grid(row=1, column=1, padx=10, pady=10)
entry2.grid(row=1, column=2, padx=10, pady=10)
lable.grid(row=1, column=3, padx=10, pady=10)

button_upoad_the_image.grid(row=2, column=0, padx=10, pady=10)
button_transtate_to_the_text.grid(row=2, column=1, padx=10, pady=10)
button_preview_image.grid(row=2, column=2, padx=10, pady=10)
button_text_to_the_txt_file.grid(row=2, column=3, padx=10, pady=10)
lable_image.grid(row=2, column=4, padx=10, pady=10)
#temp_button.grid(row=2, column=1, padx=10, pady=10)

text_box_metods_OCR.grid(row=0, column=4, padx=10, pady=10)
text_end_result.grid(row=1, column=4, padx=10, pady=10)

text_box_metods_OCR.insert(tk.END, ' ')
text_end_result.insert(tk.END, ' ')

root.mainloop()
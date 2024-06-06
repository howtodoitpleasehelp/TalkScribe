from tkinter import *
from tkinter import filedialog, font, colorchooser
from tkinter.ttk import Combobox

root = Tk()
root.title('TalkScribe')
root.iconbitmap('D:\\Clone\\CMSC_141_TextEditorProject\\icon\\text.ico')
root.geometry("1200x660")

# Set variable for open file
global open_status_name
open_status_name = False

global selected
selected = False

# Create New File
def new_file():
    # Delete previous text
    my_text.delete("1.0", END)
    # Update status bars
    root.title('New File - TalkScribe')
    status_bar.config(text="New File        ")

    global open_status_name
    open_status_name = False

# Open Files
def open_file():
    # Delete previous text
    my_text.delete("1.0", END)

    # Grab Filename
    text_file = filedialog.askopenfilename(initialdir="C:\\Users\\    ", title="Open File", filetypes=(("Text Files", "*.txt"), ("PDF Files", "*.pdf"), ("HTML Files", "*.html"), ("Python Files","*.py"),("All Files", "*.*")))
    
    # Check to see if there is a filename 
    if text_file:
        # Make filename global for access later
        global open_status_name
        open_status_name = text_file

    # Update Status bars
    name = text_file
    status_bar.config(text=f'{name}         ')
    name = name.replace("C:\\Users\\", "")
    root.title(f'{name} - TalkScribe')

    # Open File
    text_file = open(text_file, 'r')
    stuff = text_file.read()
    # Add file to textbox
    my_text.insert(END, stuff)
    # Close the opened file
    text_file.close()

# Save as File
def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:\\Users\\", title="Save File", filetypes=(("Text Files", "*.txt"), ("PDF Files", "*.pdf"), ("HTML Files", "*.html"), ("Python Files","*.py"),("All Files", "*.*")))
    if text_file:
        # Update Status Bars
        name = text_file
        status_bar.config(text=f'Saved: {name}         ')
        name = name.replace("C:\\Users\\", "")
        root.title(f'{name} - TalkScribe')

        # Save the File
        text_file = open(text_file, "w")
        text_file.write(my_text.get(1.0, END))
        # Close file
        text_file.close()

# Save File
def save_file():
    global open_status_name
    if open_status_name:
        # Save the File
        text_file = open(open_status_name, "w")
        text_file.write(my_text.get(1.0, END))
        # Close file
        text_file.close()
        # Put status update or popup code
        status_bar.config(text=f'Saved: {open_status_name}         ')
    else:
        save_as_file()

# Cut Text
def cut_text(e):
    global selected
    # check to see if we used keyboard shortcuts
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            # Grab selected text from text box
            selected = my_text.selection_get()
            # delete selected text from text box
            my_text.delete("sel.first", "sel.last")
            # clear the clipboard  then append
            root.clipboard_clear()
            root.clipboard_append(selected)

# Copy Text
def copy_text(e):
    global selected
    # check to see if we used keyboard shortcuts
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        # Grab selected text from text box
        selected = my_text.selection_get()
        # clear the clipboard  then append
        root.clipboard_clear()
        root.clipboard_append(selected)

# Paste Text
def paste_text(e):
    global selected
    # check to see if we used keyboard shortcuts
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)

# Undo and Redo functions
def undo_text(e=None):
    my_text.edit_undo()

def redo_text(e=None):
    my_text.edit_redo()

# Create Main Frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# Create Scroll Bar for Textbox
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

hor_scroll = Scrollbar(my_frame, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

# Create Text Box
my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16), selectbackground="#ACF5BC", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, wrap="none", xscrollcommand=hor_scroll.set)
my_text.pack()

# Configure Scrollbar
text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add File Menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Add Edit Menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut   (CTRL+X)", command=lambda: cut_text(False))
edit_menu.add_command(label="Copy   (CTRL+C)", command=lambda: copy_text(False))
edit_menu.add_command(label="Paste   (CTRL+V)", command=lambda: paste_text(False))
edit_menu.add_command(label="Undo   (CTRL+Z)", command=undo_text)
edit_menu.add_command(label="Redo   (CTRL+Y)", command=redo_text)

# Create Toolbar Frame
toolbar_frame = Frame(root, bd=1, relief=RIDGE)
toolbar_frame.pack(fill=X, padx=5, pady=5)

# Undo Button
undo_img = PhotoImage(file="undo.png")  # Replace "undo.png" with the name of your undo image file
undo_button = Button(toolbar_frame, image=undo_img, command=undo_text)
undo_button.image = undo_img
undo_button.pack(side=LEFT, padx=2)

# Redo Button
redo_img = PhotoImage(file="redo.png")  # Replace "redo.png" with the name of your redo image file
redo_button = Button(toolbar_frame, image=redo_img, command=redo_text)
redo_button.image = redo_img
redo_button.pack(side=LEFT, padx=2)

# Font Dropdown
font_tuple = font.families()
font_var = StringVar()
font_combobox = Combobox(toolbar_frame, textvariable=font_var, state='readonly', values=font_tuple, width=30)
font_combobox.set('Helvetica')  # Default font
font_combobox.pack(side=LEFT, padx=2)

# Font Size Dropdown
size_var = IntVar()
font_size = Combobox(toolbar_frame, textvariable=size_var, state='readonly', values=tuple(range(8, 80, 2)), width=5)
font_size.current(4)  # Default size 16
font_size.pack(side=LEFT, padx=2)

# Style Dropdown
style_var = StringVar()
style_combobox = Combobox(toolbar_frame, textvariable=style_var, state='readonly', values=('Normal', 'Bold', 'Italic', 'Underline'), width=10)
style_combobox.current(0)
style_combobox.pack(side=LEFT, padx=2)

# Bold Button
bold_img = PhotoImage(file="bold.png")  # Replace "bold.png" with the name of your bold image file
bold_button = Button(toolbar_frame, image=bold_img)
bold_button.image = bold_img
bold_button.pack(side=LEFT, padx=2)

# Italic Button
italic_img = PhotoImage(file="italic.png")  # Replace "italic.png" with the name of your italic image file
italic_button = Button(toolbar_frame, image=italic_img)
italic_button.image = italic_img
italic_button.pack(side=LEFT, padx=2)

# Underline Button
underline_img = PhotoImage(file="underline.png")  # Replace "underline.png" with the name of your underline image file
underline_button = Button(toolbar_frame, image=underline_img)
underline_button.image = underline_img
underline_button.pack(side=LEFT, padx=2)

# Text Color Button
text_color_img = PhotoImage(file="text_color.png")  # Replace "text_color.png" with the name of your text color image file
text_color_button = Button(toolbar_frame, image=text_color_img)
text_color_button.image = text_color_img
text_color_button.pack(side=LEFT, padx=2)

# Highlight Color Button
highlight_img = PhotoImage(file="highlight.png")  # Replace "highlight.png" with the name of your highlight image file
highlight_button = Button(toolbar_frame, image=highlight_img)
highlight_button.image = highlight_img
highlight_button.pack(side=LEFT, padx=2)

# Place Widgets in Toolbar Frame
undo_button.grid(row=0, column=0, padx=5, pady=5)
redo_button.grid(row=0, column=1, padx=5, pady=5)
font_combobox.grid(row=0, column=2, padx=5, pady=5)
font_size.grid(row=0, column=3, padx=5, pady=5)
style_combobox.grid(row=0, column=4, padx=5, pady=5)
bold_button.grid(row=0, column=5, padx=5, pady=5)
italic_button.grid(row=0, column=6, padx=5, pady=5)
underline_button.grid(row=0, column=7, padx=5, pady=5)
text_color_button.grid(row=0, column=8, padx=5, pady=5)
highlight_button.grid(row=0, column=9, padx=5, pady=5)

# Add Status Bar to Bottom of App
status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)

# Edit Bindings
root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)
root.bind('<Control-Key-z>', undo_text)
root.bind('<Control-Key-y>', redo_text)

root.mainloop()

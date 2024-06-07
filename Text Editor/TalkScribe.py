from tkinter import *
from tkinter import filedialog, font, colorchooser
from tkinter.ttk import Combobox
from PIL import Image, ImageTk

root = Tk()
root.title('TalkScribe')
root.iconbitmap('D:\\Clone\\CMSC_141_TextEditorProject\\icon\\text.ico')
root.geometry("1200x660")

# Set variable for open file
global open_status_name
open_status_name = False
highlight_color = None
highlight_active = False

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
    text_file = filedialog.askopenfilename(initialdir="C:\\Users\\", title="Open File", filetypes=(("Text Files", "*.txt"), ("PDF Files", "*.pdf"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    
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
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:\\Users\\", title="Save File", filetypes=(("Text Files", "*.txt"), ("PDF Files", "*.pdf"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
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
            # Split the selected text into words
            words = selected.split()
            for word in words:
                # Insert each word with a space
                my_text.insert(position, word + " ")
                # Move the position to the end of the inserted word
                position = my_text.index(f"{position} + {len(word)} chars")

# Undo and Redo functions
def undo_text(e=None):
    my_text.edit_undo()

def redo_text(e=None):
    my_text.edit_redo()

# Text Color Function
def text_color():
    selected_text_color = colorchooser.askcolor()[1]
    if selected_text_color:
        if my_text.tag_ranges("sel"):
            my_text.tag_add("text_color", SEL_FIRST, SEL_LAST)
            my_text.tag_configure("text_color", foreground=selected_text_color)
        else:
            my_text.config(fg=selected_text_color)

# Function to change font size
def change_font_size(event=None):
    try:
        new_size = int(font_size_var.get())
        if my_text.tag_ranges("sel"):
            my_text.tag_add("font_size", "sel.first", "sel.last")
            my_text.tag_configure("font_size", font=(None, new_size))
        else:
            font_style = font.Font(font=my_text['font'])
            font_style.config(size=new_size)
            my_text.tag_configure("font_size", font=(None, new_size))
    except ValueError:
        pass  # Ignore if the value is not an integer

# Function to change font style
def change_font_style(event=None):
    try:
        new_font = font_var.get()
        if my_text.tag_ranges("sel"):
            start, end = my_text.tag_ranges("sel")
            current_tags = my_text.tag_names(start)
            if "font_style" in current_tags:
                my_text.tag_remove("font_style", start, end)
            my_text.tag_add("font_style", start, end)
            my_text.tag_configure("font_style", font=(new_font, current_font_size))
            if highlight_active:
                my_text.tag_add("highlighted_text", start, end)
                my_text.tag_configure("highlighted_text", background=highlight_color)
        else:
            font_style = font.Font(font=my_text['font'])
            font_style.config(family=new_font)
            my_text.config(font=font_style)
    except ValueError:
        pass  # Ignore if the value is not a font family


# Function to change font style
def change_font_style(event=None):
    try:
        new_font = font_var.get()
        if my_text.tag_ranges("sel"):
            my_text.tag_add("font_style", SEL_FIRST, SEL_LAST)
            my_text.tag_configure("font_style", font=(new_font, current_font_size))
        else:
            font_style = font.Font(font=my_text['font'])
            font_style.config(family=new_font)
            my_text.config(font=font_style)
    except ValueError:
        pass  # Ignore if the value is not a font family

# Font Style Function
def change_font_style(event, style):
    # Check if any text is selected
    if my_text.tag_ranges("sel"):
        start, end = my_text.tag_ranges("sel")
        current_tags = my_text.tag_names(start)
        if style == "Bold":
            if "bold" in current_tags:
                my_text.tag_remove("bold", start, end)
            else:
                if "italic" in current_tags:
                    my_text.tag_remove("italic", start, end)
                if "underline" in current_tags:
                    my_text.tag_remove("underline", start, end)
                my_text.tag_add("bold", start, end)
                my_text.tag_configure("bold", font=('Helvetica', 16, 'bold'))
        elif style == "Italic":
            if "italic" in current_tags:
                my_text.tag_remove("italic", start, end)
            else:
                if "bold" in current_tags:
                    my_text.tag_remove("bold", start, end)
                if "underline" in current_tags:
                    my_text.tag_remove("underline", start, end)
                my_text.tag_add("italic", start, end)
                my_text.tag_configure("italic", font=('Helvetica', 16, 'italic'))
        elif style == "Underline":
            if "underline" in current_tags:
                my_text.tag_remove("underline", start, end)
            else:
                if "bold" in current_tags:
                    my_text.tag_remove("bold", start, end)
                if "italic" in current_tags:
                    my_text.tag_remove("italic", start, end)
                my_text.tag_add("underline", start, end)
                my_text.tag_configure("underline", font=('Helvetica', 16, 'underline'))
    else:
        # Get current position
        current_pos = my_text.index(INSERT)
        # Get the content of the line where the cursor is
        line_start = my_text.index(f"{current_pos} linestart")
        line_end = my_text.index(f"{current_pos} lineend")
        current_line = my_text.get(line_start, line_end)

        # If there is content, the text will be added in the current position
        if current_line.strip():
            my_text.insert(INSERT, " ", "bold")
            my_text.tag_add("bold", INSERT + "-1c", INSERT)
            my_text.insert(INSERT, " ", "bold")
            my_text.tag_add("bold", INSERT + "-1c", INSERT)

        my_text.tag_configure("bold", font=('Helvetica', 16, 'bold'))

# Style Dropdown Function
def change_text_style(event=None):
    try:
        new_style = style_var.get()
        if my_text.tag_ranges("sel"):
            start, end = my_text.tag_ranges("sel")
            current_tags = my_text.tag_names(start)
            for tag in current_tags:
                my_text.tag_remove(tag, start, end)
            if new_style == 'Title':
                my_text.tag_add("title", start, end)
                my_text.tag_configure("title", font=('Helvetica', 24, 'bold'))
            elif new_style == 'Heading 1':
                my_text.tag_add("heading1", start, end)
                my_text.tag_configure("heading1", font=('Helvetica', 20, 'bold'))
            elif new_style == 'Heading 2':
                my_text.tag_add("heading2", start, end)
                my_text.tag_configure("heading2", font=('Helvetica', 18, 'bold'))
            elif new_style == 'Heading 3':
                my_text.tag_add("heading3", start, end)
                my_text.tag_configure("heading3", font=('Helvetica', 16, 'bold'))
            else:
                my_text.tag_add("normal", start, end)
                my_text.tag_configure("normal", font=('Helvetica', 14))
        else:
            current_pos = my_text.index(INSERT)
            line_start = my_text.index(f"{current_pos} linestart")
            line_end = my_text.index(f"{current_pos} lineend")
            current_line = my_text.get(line_start, line_end)
            if current_line.strip():
                if new_style == 'Title':
                    my_text.insert(INSERT, "\n\n", "title")
                    my_text.tag_add("title", INSERT + "-2l", INSERT + "-1l lineend")
                    my_text.insert(INSERT, "\n\n")
                    my_text.tag_add("title", INSERT + "-2l", INSERT + "-1l lineend")
                    my_text.tag_configure("title", font=('Helvetica', 24, 'bold'))
                elif new_style == 'Heading 1':
                    my_text.insert(INSERT, "\n\n", "heading1")
                    my_text.tag_add("heading1", INSERT + "-2l", INSERT + "-1l lineend")
                    my_text.insert(INSERT, "\n\n")
                    my_text.tag_add("heading1", INSERT + "-2l", INSERT + "-1l lineend")
                    my_text.tag_configure("heading1", font=('Helvetica', 20, 'bold'))
                elif new_style == 'Heading 2':
                    my_text.insert(INSERT, "\n\n", "heading2")
                    my_text.tag_add("heading2", INSERT + "-2l", INSERT + "-1l lineend")
                    my_text.insert(INSERT, "\n\n")
                    my_text.tag_add("heading2", INSERT + "-2l", INSERT + "-1l lineend")
                    my_text.tag_configure("heading2", font=('Helvetica', 16, 'bold'))
                elif new_style == 'Heading 3':
                    my_text.insert(INSERT, "\n\n", "heading3")
                    my_text.tag_add("heading3", INSERT + "-2l", INSERT + "-1l lineend")
                    my_text.insert(INSERT, "\n\n")
                    my_text.tag_add("heading3", INSERT + "-2l", INSERT + "-1l lineend")
                    my_text.tag_configure("heading3", font=('Helvetica', 14, 'bold'))
                else:
                    my_text.insert(INSERT, "\n\n", "normal")
                    my_text.tag_add("normal", INSERT + "-2l", INSERT + "-1l lineend")
                    my_text.insert(INSERT, "\n\n")
                    my_text.tag_add("normal", INSERT + "-2l", INSERT + "-1l lineend")
                    my_text.tag_configure("normal", font=('Helvetica', 12))
    except ValueError:
        pass  # Ignore if the value is not a style


# Highlight Text Function
def highlight_text():
    global highlight_color, highlight_active
    if highlight_active:
        highlight_active = False
        highlight_button.config(bg="SystemButtonFace")  # Change button color to default
    else:
        selected_color = colorchooser.askcolor()[1]
        if selected_color:
            highlight_color = selected_color
            highlight_active = True
            highlight_button.config(bg="lightgreen")  # Change button color when active

    if highlight_active:
        my_text.tag_add("highlighted_text", "sel.first", "sel.last")
        my_text.tag_configure("highlighted_text", background=highlight_color)

# Unhighlight Text Function
def unhighlight_text():
    my_text.tag_remove("highlighted_text", "1.0", END)
    global highlight_active
    highlight_active = False
    highlight_button.config(bg="SystemButtonFace")  # Change button color to default

# Function to align text
def align_text(align_type):
    if my_text.tag_ranges("sel"):
        start, end = my_text.tag_ranges("sel")
        current_tags = my_text.tag_names(start)
        if "align" in current_tags:
            my_text.tag_remove("align", start, end)
        my_text.tag_add("align", start, end)
        my_text.tag_configure("align", justify=align_type)
        if align_type == "justify":
            # Get the text content
            text_content = my_text.get(start, end)
            # Calculate the number of spaces to add between words
            spaces_to_add = text_content.count(" ")
            # Add the necessary spaces to justify the text
            for _ in range(spaces_to_add):
                my_text.insert(end, " ")
    else:
        # Get current position
        current_pos = my_text.index(INSERT)
        # Get the content of the line where the cursor is
        line_start = my_text.index(f"{current_pos} linestart")
        line_end = my_text.index(f"{current_pos} lineend")
        current_line = my_text.get(line_start, line_end)

        # If there is content, the text will be added in the current position
        if current_line.strip():
            my_text.insert(INSERT, " ", "align")
            my_text.tag_add("align", INSERT + "-1c", INSERT)
            my_text.insert(INSERT, " ", "align")
            my_text.tag_add("align", INSERT + "-1c", INSERT)

        my_text.tag_configure("align", justify=align_type)


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

# Add Format Menu
format_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Format", menu=format_menu)

# Add Line Spacing Submenu
line_spacing_menu = Menu(format_menu, tearoff=False)
format_menu.add_cascade(label="Line Spacing", menu=line_spacing_menu)
line_spacing_menu.add_radiobutton(label="Single", command=lambda: change_line_spacing(1))
line_spacing_menu.add_radiobutton(label="1.5", command=lambda: change_line_spacing(1.5))
line_spacing_menu.add_radiobutton(label="Double-Spaced", command=lambda: change_line_spacing("2"))

# Add Paragraph Spacing Submenu
paragraph_spacing_menu = Menu(format_menu, tearoff=False)
format_menu.add_cascade(label="Paragraph Spacing", menu=paragraph_spacing_menu)
paragraph_spacing_menu.add_radiobutton(label="Before: 0, After: 0", command=lambda: change_paragraph_spacing(0, 0))
paragraph_spacing_menu.add_radiobutton(label="Before: 6, After: 6", command=lambda: change_paragraph_spacing(6, 6))
paragraph_spacing_menu.add_radiobutton(label="Before: 12, After: 12", command=lambda: change_paragraph_spacing(12, 12))
paragraph_spacing_menu.add_radiobutton(label="Before: 24, After: 24", command=lambda: change_paragraph_spacing(24, 24))

# Function to change line spacing
def change_line_spacing(value):
    if value == "double":
        spacing = 24  # Double-spaced
    else:
        spacing = value
    if my_text.tag_ranges("sel"):
        start, end = my_text.tag_ranges("sel")
        my_text.tag_configure("spacing1", spacing1=spacing)
        my_text.tag_add("spacing1", start, end)
    else:
        my_text.config(spacing1=spacing)

# Function to change paragraph spacing
def change_paragraph_spacing(before, after):
    if my_text.tag_ranges("sel"):
        start, end = my_text.tag_ranges("sel")
        my_text.tag_configure("spacing2", spacing2=(before, after))
        my_text.tag_add("spacing2", start, end)
    else:
        my_text.config(spacing2=(before, after))

# Function to increase line spacing
def increase_line_spacing():
    current_spacing = my_text.config('spacing1')[-1]
    if current_spacing == "double":
        new_spacing = 120  # Double the size of single spaced
    else:
        new_spacing = current_spacing * 2
    change_line_spacing(new_spacing)

# Function to increase paragraph spacing
def increase_paragraph_spacing():
    current_spacing = my_text.config('spacing2')[-1][1]
    new_spacing = current_spacing * 2
    change_paragraph_spacing(new_spacing, new_spacing)


# Function to add tooltip for buttons
def add_tooltip(widget, text):
    Tooltip(widget, text)

# Tooltip class
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
        self.tooltip = None

    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = Label(self.tooltip, text=self.text, background="lightyellow", relief="solid", borderwidth=1, font=("Helvetica", 10))
        label.pack(ipadx=5)

    def close(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()

# Create Toolbar Frame
toolbar_frame = Frame(root, bd=1, relief=RIDGE)
toolbar_frame.pack(fill=X, padx=5, pady=5)

# Undo Button
undo_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\undo.ico")
undo_img = undo_img.resize((16, 16))
undo_img = ImageTk.PhotoImage(undo_img)
undo_button = Button(toolbar_frame, image=undo_img, command=undo_text)
undo_button.image = undo_img
undo_button.pack(side=LEFT, padx=2, pady=2)
add_tooltip(undo_button, "Undo")

# Redo Button
redo_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\redo.ico")
redo_img = redo_img.resize((16, 16))
redo_img = ImageTk.PhotoImage(redo_img)
redo_button = Button(toolbar_frame, image=redo_img, command=redo_text)
redo_button.image = redo_img
redo_button.pack(side=LEFT, padx=2, pady=2)
add_tooltip(redo_button, "Redo")

# Font Dropdown
font_tuple = font.families()
font_var = StringVar()
font_combobox = Combobox(toolbar_frame, textvariable=font_var, state='readonly', values=font_tuple, width=30)
font_combobox.set('Helvetica')  # Default font
font_combobox.pack(side=LEFT, padx=2, pady=2)
font_combobox.bind("<<ComboboxSelected>>", change_font_style)
add_tooltip(font_combobox, "Font Style")

# Font Size Dropdown
font_size_var = StringVar()
font_size_combobox = Combobox(toolbar_frame, textvariable=font_size_var, values=[i for i in range(8, 80)], state='readonly', width=5)
font_size_combobox.set(16)  # default font size
font_size_combobox.pack(side=LEFT, padx=2, pady=2)
font_size_combobox.bind("<<ComboboxSelected>>", change_font_size)
add_tooltip(font_size_combobox, "Font Size")

# Style Dropdown
style_var = StringVar()
style_combobox = Combobox(toolbar_frame, textvariable=style_var, state='readonly', values=('Normal', 'Title', 'Heading 1', 'Heading 2', 'Heading 3'), width=10)
style_combobox.current(0)
style_combobox.pack(side=LEFT, padx=2, pady=2)
style_combobox.bind("<<ComboboxSelected>>", change_text_style)
add_tooltip(style_combobox, "Text Style")

# Bold Button
bold_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\bold.ico")
bold_img = bold_img.resize((16, 16))
bold_img = ImageTk.PhotoImage(bold_img)
bold_button = Button(toolbar_frame, image=bold_img, command=lambda: change_font_style(None, "Bold"))
bold_button.image = bold_img
bold_button.pack(side=LEFT, padx=2, pady=2)
add_tooltip(bold_button, "Bold")

# Italic Button
italic_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\italic.ico")
italic_img = italic_img.resize((16, 16))
italic_img = ImageTk.PhotoImage(italic_img)
italic_button = Button(toolbar_frame, image=italic_img, command=lambda: change_font_style(None, "Italic"))
italic_button.image = italic_img
italic_button.pack(side=LEFT, padx=2, pady=2)
add_tooltip(italic_button, "Italic")

# Underline Button
underline_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\underline.ico")
underline_img = underline_img.resize((16, 16))
underline_img = ImageTk.PhotoImage(underline_img)
underline_button = Button(toolbar_frame, image=underline_img, command=lambda: change_font_style(None, "Underline"))
underline_button.image = underline_img
underline_button.pack(side=LEFT, padx=2, pady=2)
add_tooltip(underline_button, "Underline")

# Text Color Button
text_color_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\text_color.ico")
text_color_img = text_color_img.resize((16, 16))
text_color_img = ImageTk.PhotoImage(text_color_img)
text_color_button = Button(toolbar_frame, image=text_color_img, command=text_color)
text_color_button.image = text_color_img
text_color_button.pack(side=LEFT, padx=2, pady=2)
add_tooltip(text_color_button, "Text Color")

# Highlight Color Button
highlight_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\highlight.ico")
highlight_img = highlight_img.resize((16, 16))
highlight_img = ImageTk.PhotoImage(highlight_img)
highlight_button = Button(toolbar_frame, image=highlight_img, command=highlight_text)
highlight_button.image = highlight_img
highlight_button.pack(side=LEFT, padx=2, pady=2)
add_tooltip(highlight_button, "Highlight")

# Unhighlight Button
unhighlight_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\unhighlight.ico")
unhighlight_img = unhighlight_img.resize((16, 16))
unhighlight_img = ImageTk.PhotoImage(unhighlight_img)
unhighlight_button = Button(toolbar_frame, image=unhighlight_img, command=unhighlight_text)
unhighlight_button.image = unhighlight_img
unhighlight_button.pack(side=LEFT, padx=2, pady=2)
add_tooltip(unhighlight_button, "Remove Highlight")

# Align Left Button
align_left_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\align_left.ico")
align_left_img = align_left_img.resize((16, 16))
align_left_img = ImageTk.PhotoImage(align_left_img)
align_left_button = Button(toolbar_frame, image=align_left_img, command=lambda: align_text("left"))
align_left_button.image = align_left_img
align_left_button.pack(side=LEFT, padx=2, pady=2)
add_tooltip(align_left_button, "Align Left")

# Align Center Button
align_center_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\align_center.ico")
align_center_img = align_center_img.resize((16, 16))
align_center_img = ImageTk.PhotoImage(align_center_img)
align_center_button = Button(toolbar_frame, image=align_center_img, command=lambda: align_text("center"))
align_center_button.image = align_center_img
align_center_button.pack(side=LEFT, padx=2, pady=2)
add_tooltip(align_center_button, "Align Center")

# Align Right Button
align_right_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\align_right.ico")
align_right_img = align_right_img.resize((16, 16))
align_right_img = ImageTk.PhotoImage(align_right_img)
align_right_button = Button(toolbar_frame, image=align_right_img, command=lambda: align_text("right"))
align_right_button.image = align_right_img
align_right_button.pack(side=LEFT, padx=2, pady=2)
add_tooltip(align_right_button, "Align Right")

# Justify Button
justify_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\justify.ico")
justify_img = justify_img.resize((16, 16))
justify_img = ImageTk.PhotoImage(justify_img)
justify_button = Button(toolbar_frame, image=justify_img, command=lambda: align_text("justify"))
justify_button.image = justify_img
justify_button.pack(side=LEFT, padx=2, pady=2)
add_tooltip(justify_button, "Justify")

# Function to add tooltip for buttons
def add_tooltip(widget, text):
    Tooltip(widget, text)

# Tooltip class
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
        self.tooltip = None

    def enter(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = Label(self.tooltip, text=self.text, background="lightyellow", relief="solid", borderwidth=1, font=("Helvetica", 10))
        label.pack(ipadx=5)

    def close(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()

# Create Main Frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# Create Scroll Bar for Textbox
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

hor_scroll = Scrollbar(my_frame, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

# Create Text Box
my_text = Text(my_frame, width=80, height=40, font=("Helvetica", 16), selectbackground="#ACF5BC", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, xscrollcommand=hor_scroll.set)
my_text.pack()

# Configure Scrollbar
text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

# Place Widgets in Toolbar Frame
undo_button.pack(side=LEFT, padx=2, pady=2)
redo_button.pack(side=LEFT, padx=2, pady=2)
font_combobox.pack(side=LEFT, padx=2, pady=2)
font_size_combobox.pack(side=LEFT, padx=2, pady=2)
style_combobox.pack(side=LEFT, padx=2, pady=2)
bold_button.pack(side=LEFT, padx=2, pady=2)
italic_button.pack(side=LEFT, padx=2, pady=2)
underline_button.pack(side=LEFT, padx=2, pady=2)
text_color_button.pack(side=LEFT, padx=2, pady=2)
highlight_button.pack(side=LEFT, padx=2, pady=2)


# Edit Bindings
root.bind('<Control-x>', lambda event: cut_text(True))
root.bind('<Control-c>', lambda event: copy_text(True))
root.bind('<Control-v>', lambda event: paste_text(True))
root.bind('<Control-z>', undo_text)
root.bind('<Control-y>', redo_text)
root.bind('<Control-b>', lambda event: change_font_style(None, "Bold"))
root.bind('<Control-Shift-b>', lambda event: change_font_style(None, "Bold"))
root.bind('<Control-Alt-i>', lambda event: change_font_style(None, "Italic"))
root.bind('<Control-Shift-i>', lambda event: change_font_style(None, "Italic"))
root.bind('<Control-u>', lambda event: change_font_style(None, "Underline"))
root.bind('<Control-Shift-u>', lambda event: change_font_style(None, "Underline"))
root.bind('<Control-h>', lambda event: highlight_text())

# Add Status Bar to Bottom of App
status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)


root.mainloop()


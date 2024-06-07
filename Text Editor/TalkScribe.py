import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, font, colorchooser, Button, INSERT
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import pyaudio


root = tk.Tk()
root.title('TalkScribe')
root.iconbitmap('D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\text.ico')
root.geometry("1200x660")

# Set variable for open file
global open_status_name
open_status_name = False
highlight_color = None
highlight_active = False

global selected
selected = False

global microphone_active
microphone_active = False

global current_font_size
current_font_size = 16

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

    # Update the status bar
    status_bar = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

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
def change_font(event=None):
    try:
        new_font = font_var.get()
        if my_text.tag_ranges("sel"):
            start, end = my_text.tag_ranges("sel")
            my_text.tag_add("font_style", start, end)
            my_text.tag_configure("font_style", font=(new_font, current_font_size))
            if highlight_active:
                my_text.tag_add("highlighted_text", start, end)
                my_text.tag_configure("highlighted_text", font=(new_font, current_font_size), background=highlight_color)
        else:
            font_style = font.Font(font=my_text['font'])
            font_style.config(family=new_font)
            my_text.config(font=font_style)
        
        # Reapply the current font size to prevent the size change
        my_text.tag_configure("font_style", font=(new_font, current_font_size))

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
            # Remove the right align tag if it exists
            my_text.tag_remove("align", f"{current_pos} linestart", f"{current_pos} lineend")
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


# Function to use speech-to-text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        status_bar.config(text="Listening...")
        root.update()
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            my_text.insert(END, text)
            status_bar.config(text="Speech-to-Text Successful")
        except Exception as e:
            print(e)
            status_bar.config(text="Speech-to-Text Failed")

def toggle_microphone():
    global microphone_active
    engine = pyttsx3.init() 
    if microphone_active:
        microphone_active = False
        mic_button.config(image=mic_icon)
        mic_button.config(command=microphone_start)
        add_tooltip(mic_button, "Turn on Speech-to-Text")
        status_bar.config(text="Speech-to-Text Turned Off")
        engine.say("Speech-to-Text turned off")
        engine.runAndWait()
    else:
        microphone_active = True
        mic_button.config(image=mic_active)
        mic_button.config(command=toggle_microphone)  # Change here
        add_tooltip(mic_button, "Turn off Speech-to-Text")  # Change here
        status_bar.config(text="Listening...")
        engine.say("Listening")
        engine.runAndWait()
        microphone_start()

def microphone_on():
    global microphone_active
    microphone_active = True
    mic_button.config(image=mic_active)
    r = sr.Recognizer()
    engine = pyttsx3.init()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while microphone_active:
            status_bar.config(text="Listening...")
            root.update()
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                my_text.insert(INSERT, text + ' ')
                engine.say(text)
                engine.runAndWait()
                status_bar.config(text="Speech-to-Text Successful")
            except sr.UnknownValueError:
                error_msg = "TalkScribe could not understand audio"
                print(error_msg)
                engine.say(error_msg)
                engine.runAndWait()
                status_bar.config(text="Speech-to-Text Failed")
            except sr.RequestError as e:
                error_msg = "Could not request results from Google Speech Recognition service; {0}".format(e)
                print(error_msg)
                engine.say(error_msg)
                engine.runAndWait()
                status_bar.config(text="Speech-to-Text Failed")
            except Exception as e:
                print(e)
                engine.say("An error occurred")
                status_bar.config(text="Speech-to-Text Failed")
        mic_button.config(image=mic_icon)
        mic_button.config(command=toggle_microphone)
        add_tooltip(mic_button, "Turn off Speech-to-Text")
        status_bar.config(text="Speech-to-Text Turned Off")

def microphone_off():
    global microphone_active
    microphone_active = False
    mic_button.config(image=mic_icon)
    mic_button.config(command=toggle_microphone)  # Change here
    add_tooltip(mic_button, "Turn on Speech-to-Text")  # Change here
    status_bar.config(text="Speech-to-Text Turned Off")

def microphone_start():
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                if "hey" in text.lower():  # Change "hello" to your desired keyword
                    toggle_microphone()
                elif "thank you" in text.lower():  # Change "goodbye" to your desired keyword to turn off the microphone
                    microphone_off()
            except Exception as e:
                print(e)


# Create Menu
my_menu = tk.Menu(root, background='#AAD4C1')
#my_menu.configure(background='#F5F6E2')
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

# Add Status Bar to Bottom of App
status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=Y, side=BOTTOM, ipady=5)


# Create Toolbar Frame
toolbar_frame = Frame(root, bd=1, relief=RIDGE, bg="#D9E0C5")
toolbar_frame.pack(fill=X, padx=5, pady=5)

button_shade = "#D9E0C5"

# Configure the style for TCombobox
style = ttk.Style()
style.configure('TCombobox', fieldbackground=button_shade, background=button_shade)


# Undo Button
undo_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\undo.ico")
undo_img = undo_img.resize((16, 16))
undo_img = ImageTk.PhotoImage(undo_img)
undo_button = tk.Button(toolbar_frame, image=undo_img, command=undo_text, bg=button_shade)
undo_button.image = undo_img
undo_button.pack(side=tk.LEFT, padx=2, pady=2)
add_tooltip(undo_button, "Undo")

# Redo Button
redo_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\redo.ico")
redo_img = redo_img.resize((16, 16))
redo_img = ImageTk.PhotoImage(redo_img)
redo_button = tk.Button(toolbar_frame, image=redo_img, command=redo_text, bg=button_shade)
redo_button.image = redo_img
redo_button.pack(side=tk.LEFT, padx=2, pady=2)
add_tooltip(redo_button, "Redo")

# Font Dropdown
font_tuple = tk.font.families()
font_var = tk.StringVar()
font_combobox = ttk.Combobox(toolbar_frame, textvariable=font_var, state='readonly', values=font_tuple, width=30)
font_combobox.set('Helvetica')  # Default font
font_combobox.pack(side=tk.LEFT, padx=2, pady=2)
font_combobox.bind("<<ComboboxSelected>>", change_font)
add_tooltip(font_combobox, "Font Style")

# Font Size Dropdown
font_size_var = tk.StringVar()
font_size_combobox = ttk.Combobox(toolbar_frame, textvariable=font_size_var, values=[i for i in range(8, 80)], state='readonly', width=5)
font_size_combobox.set(16)  # Default font size
font_size_combobox.pack(side=tk.LEFT, padx=2, pady=2)
font_size_combobox.bind("<<ComboboxSelected>>", change_font_size)
add_tooltip(font_size_combobox, "Font Size")

# Style Dropdown
style_var = tk.StringVar()
style_combobox = ttk.Combobox(toolbar_frame, textvariable=style_var, state='readonly', values=('Normal', 'Title', 'Heading 1', 'Heading 2', 'Heading 3'), width=10)
style_combobox.current(0)
style_combobox.pack(side=tk.LEFT, padx=2, pady=2)
style_combobox.bind("<<ComboboxSelected>>", change_text_style)
add_tooltip(style_combobox, "Text Style")

# Bold Button
bold_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\bold.ico")
bold_img = bold_img.resize((16, 16))
bold_img = ImageTk.PhotoImage(bold_img)
bold_button = tk.Button(toolbar_frame, image=bold_img, command=lambda: change_font_style(None, "Bold"), bg=button_shade)
bold_button.image = bold_img
bold_button.pack(side=tk.LEFT, padx=2, pady=2)
add_tooltip(bold_button, "Bold")

# Italic Button
italic_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\italic.ico")
italic_img = italic_img.resize((16, 16))
italic_img = ImageTk.PhotoImage(italic_img)
italic_button = tk.Button(toolbar_frame, image=italic_img, command=lambda: change_font_style(None, "Italic"), bg=button_shade)
italic_button.image = italic_img
italic_button.pack(side=tk.LEFT, padx=2, pady=2)
add_tooltip(italic_button, "Italic")

# Underline Button
underline_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\underline.ico")
underline_img = underline_img.resize((16, 16))
underline_img = ImageTk.PhotoImage(underline_img)
underline_button = tk.Button(toolbar_frame, image=underline_img, command=lambda: change_font_style(None, "Underline"), bg=button_shade)
underline_button.image = underline_img
underline_button.pack(side=tk.LEFT, padx=2, pady=2)
add_tooltip(underline_button, "Underline")

# Text Color Button
text_color_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\text_color.ico")
text_color_img = text_color_img.resize((16, 16))
text_color_img = ImageTk.PhotoImage(text_color_img)
text_color_button = tk.Button(toolbar_frame, image=text_color_img, command=text_color, bg=button_shade)
text_color_button.image = text_color_img
text_color_button.pack(side=tk.LEFT, padx=2, pady=2)
add_tooltip(text_color_button, "Text Color")

# Highlight Color Button
highlight_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\highlight.ico")
highlight_img = highlight_img.resize((16, 16))
highlight_img = ImageTk.PhotoImage(highlight_img)
highlight_button = tk.Button(toolbar_frame, image=highlight_img, command=highlight_text, bg=button_shade)
highlight_button.image = highlight_img
highlight_button.pack(side=tk.LEFT, padx=2, pady=2)
add_tooltip(highlight_button, "Highlight")

# Unhighlight Button
unhighlight_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\unhighlight.ico")
unhighlight_img = unhighlight_img.resize((16, 16))
unhighlight_img = ImageTk.PhotoImage(unhighlight_img)
unhighlight_button = tk.Button(toolbar_frame, image=unhighlight_img, command=unhighlight_text, bg=button_shade)
unhighlight_button.image = unhighlight_img
unhighlight_button.pack(side=tk.LEFT, padx=2, pady=2)
add_tooltip(unhighlight_button, "Remove Highlight")

# Align Left Button
align_left_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\align_left.ico")
align_left_img = align_left_img.resize((16, 16))
align_left_img = ImageTk.PhotoImage(align_left_img)
align_left_button = tk.Button(toolbar_frame, image=align_left_img, command=lambda: align_text("left"), bg=button_shade)
align_left_button.image = align_left_img
align_left_button.pack(side=tk.LEFT, padx=2, pady=2)
add_tooltip(align_left_button, "Align Left")

# Align Center Button
align_center_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\align_center.ico")
align_center_img = align_center_img.resize((16, 16))
align_center_img = ImageTk.PhotoImage(align_center_img)
align_center_button = tk.Button(toolbar_frame, image=align_center_img, command=lambda: align_text("center"), bg=button_shade)
align_center_button.image = align_center_img
align_center_button.pack(side=tk.LEFT, padx=2, pady=2)
add_tooltip(align_center_button, "Align Center")

# Align Right Button
align_right_img = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\align_right.ico")
align_right_img = align_right_img.resize((16, 16))
align_right_img = ImageTk.PhotoImage(align_right_img)
align_right_button = tk.Button(toolbar_frame, image=align_right_img, command=lambda: align_text("right"), bg=button_shade)
align_right_button.image = align_right_img
align_right_button.pack(side=tk.LEFT, padx=2, pady=2)
add_tooltip(align_right_button, "Align Right")

# Create the microphone button
mic_active = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\mic_active.ico")
mic_active = mic_active.resize((16, 16))
mic_active = ImageTk.PhotoImage(mic_active)

mic_icon = Image.open("D:\\Clone\\CMSC_141_TextEditorProject\\Text Editor\\mic.ico")
mic_icon = mic_icon.resize((16, 16))
mic_icon = ImageTk.PhotoImage(mic_icon)

microphone_active = False

mic_button = Button(toolbar_frame, image=mic_icon, command=toggle_microphone, bg=button_shade)
mic_button.image = mic_icon
mic_button.pack(side=RIGHT, padx=2, pady=2)
add_tooltip(mic_button, "Speech-to-Text")

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

# Create Scroll Bar for Textbox
text_scroll = Scrollbar(my_frame, bg="#5C6C7D", troughcolor="#C4CBD6")
text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

hor_scroll = Scrollbar(my_frame, orient='horizontal', bg="#5C6C7D", troughcolor="#C4CBD6")
hor_scroll.pack(side=tk.BOTTOM, fill=tk.X)

# Create Text Box
my_text = Text(my_frame, width=80, height=40, font=("Helvetica", 16), selectbackground="#ACF5BC", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, xscrollcommand=hor_scroll.set)
my_text.pack()

# Configure Scrollbar
text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)


root.mainloop()


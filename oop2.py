import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font
from tkinter.scrolledtext import ScrolledText
import os

class TextEditor(tk.Tk):
    def __init__(self, filename=None):
        super().__init__()

        self.title("Text Editor")
        self.geometry("800x600")

        self.text_widget = ScrolledText(self, wrap="word", undo=True)
        self.text_widget.pack(fill="both", expand=True)

        self.menu_bar = tk.Menu(self)
        self.configure(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Undo", command=self.text_widget.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_widget.edit_redo)

        self.format_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Select Font", command=self.select_font)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

        self.bind_shortcuts()

        self.filename = None
        self.load_file(filename)

    def bind_shortcuts(self):
        self.bind_all("<Control-n>", lambda event: self.new_file())
        self.bind_all("<Control-o>", lambda event: self.open_file())
        self.bind_all("<Control-s>", lambda event: self.save_file())
        self.bind_all("<Control-Shift-s>", lambda event: self.save_file_as())
        self.bind_all("<Control-q>", lambda event: self.quit())
        self.bind_all("<Control-x>", lambda event: self.cut())
        self.bind_all("<Control-c>", lambda event: self.copy())
        self.bind_all("<Control-v>", lambda event: self.paste())
        self.bind_all("<Control-z>", lambda event: self.text_widget.edit_undo())
        self.bind_all("<Control-y>", lambda event: self.text_widget.edit_redo())

    def new_file(self):
        TextEditor()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.load_file(file_path)

    def save_file(self):
        if self.filename:
            with open(self.filename, "w") as file:
                file.write(self.text_widget.get("1.0", tk.END))
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.filename = file_path
            self.save_file()

    def load_file(self, filename):
        if filename:
            with open(filename, "r") as file:
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert(tk.END, file.read())
                self.filename = filename

    def cut(self):
        self.text_widget.event_generate("<<Cut>>")

    def copy(self):
        self.text_widget.event_generate("<<Copy>>")

    def paste(self):
        self.text_widget.event_generate("<<Paste>>")

    def select_font(self):
        selected_font = font.Font(font=self.text_widget["font"])
        new_font = font.askfont(self, font=selected_font)
        if new_font:
            self.text_widget["font"] = new_font.actual()

    def show_about(self):
        messagebox.showinfo("About", "Something about this wonderful program")


if __name__ == "__main__":
    app = TextEditor()
    app.mainloop()

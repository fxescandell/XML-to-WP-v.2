import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from funciones import process_files

class XMLtoCSVConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("XML to CSV Converter")
        self.root.geometry("800x600")  # Increase the width and height of the window
        self.create_widgets()

    def create_widgets(self):
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Helvetica", 12))

        # Create a frame to hold all widgets
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.pack(expand=True)

        self.label = ttk.Label(self.frame, text="Seleccione archivos XML:")
        self.label.pack(pady=10)

        self.select_files_btn = ttk.Button(self.frame, text="Seleccionar Archivos", command=self.select_files)
        self.select_files_btn.pack(pady=5)

        self.files_listbox = tk.Listbox(self.frame, width=80, height=10)
        self.files_listbox.pack(pady=10)

        self.label = ttk.Label(self.frame, text="Seleccione la carpeta de destino:")
        self.label.pack(pady=10)

        self.select_folder_btn = ttk.Button(self.frame, text="Seleccionar Carpeta", command=self.select_folder)
        self.select_folder_btn.pack(pady=5)

        self.folder_label = ttk.Label(self.frame, text="")
        self.folder_label.pack(pady=5)

        self.label = ttk.Label(self.frame, text="Nombre del archivo CSV:")
        self.label.pack(pady=10)

        self.csv_name_entry = ttk.Entry(self.frame, width=50)
        self.csv_name_entry.pack(pady=5)

        self.convert_btn = ttk.Button(self.frame, text="Convertir", command=self.convert)
        self.convert_btn.pack(pady=20)

    def select_files(self):
        self.file_paths = filedialog.askopenfilenames(filetypes=[("XML files", "*.xml")])
        self.files_listbox.delete(0, tk.END)  # Clear the listbox
        for file_path in self.file_paths:
            self.files_listbox.insert(tk.END, file_path)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        self.folder_label.config(text=self.folder_path)

    def convert(self):
        if not self.file_paths or not self.folder_path or not self.csv_name_entry.get():
            messagebox.showerror("Error", "Debe seleccionar archivos, una carpeta de destino y un nombre para el archivo CSV")
            return

        csv_path = f"{self.folder_path}/{self.csv_name_entry.get()}.csv"
        self.show_processing_message()
        process_files(self.file_paths, csv_path)
        self.show_completed_message()

    def show_processing_message(self):
        self.processing_label = ttk.Label(self.frame, text="Procesando...", foreground="blue")
        self.processing_label.pack(pady=10)

    def show_completed_message(self):
        self.processing_label.config(text="Completado", foreground="green")


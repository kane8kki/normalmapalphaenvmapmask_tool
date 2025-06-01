import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Set the appearance mode and color theme for customtkinter
ctk.set_appearance_mode("System")  # Can be "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Can be "blue", "dark-blue", "green"

def apply_alpha_channel(base_image_path, alpha_image_path, output_image_path):
    """
    Applique une image en noir et blanc comme canal alpha à une image de base.
    """
    try:
        base_image = Image.open(base_image_path).convert("RGBA")
        alpha_image = Image.open(alpha_image_path).convert("L") # Convert to grayscale

        # Ensure alpha image has the same size as base image
        if alpha_image.size != base_image.size:
            alpha_image = alpha_image.resize(base_image.size, Image.LANCZOS)

        # Split the base image into R, G, B, A channels
        r, g, b, a_base = base_image.split()
        
        # Merge the R, G, B channels from base_image with the new alpha_image
        rgba_image = Image.merge("RGBA", (r, g, b, alpha_image))
        rgba_image.save(output_image_path)
        return True
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue lors du traitement de l'image : {e}")
        return False

class ImageProcessorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Fusion d'images avec canal Alpha")
        self.geometry("800x700") # Increased window size for previews
        self.grid_columnconfigure(0, weight=1) # Allow column to expand

        self.base_image_path = None
        self.alpha_image_path = None
        self.output_directory = None

        # --- Frame for Base Image Selection ---
        self.base_frame = ctk.CTkFrame(self)
        self.base_frame.pack(pady=10, padx=20, fill="x")
        self.base_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.base_frame, text="Image de base (couleur) :", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)
        self.base_path_label = ctk.CTkLabel(self.base_frame, text="Aucun fichier sélectionné", text_color="gray")
        self.base_path_label.grid(row=1, column=0, padx=10, sticky="w")
        ctk.CTkButton(self.base_frame, text="Sélectionner l'image de base", command=self.select_base_image).grid(row=1, column=1, padx=10, pady=5, sticky="e")
        
        self.base_image_preview = ctk.CTkLabel(self.base_frame, text="")
        self.base_image_preview.grid(row=2, column=0, columnspan=2, pady=5)

        # --- Frame for Alpha Image Selection ---
        self.alpha_frame = ctk.CTkFrame(self)
        self.alpha_frame.pack(pady=10, padx=20, fill="x")
        self.alpha_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.alpha_frame, text="Image Noir et Blanc (canal Alpha) :", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)
        self.alpha_path_label = ctk.CTkLabel(self.alpha_frame, text="Aucun fichier sélectionné", text_color="gray")
        self.alpha_path_label.grid(row=1, column=0, padx=10, sticky="w")
        ctk.CTkButton(self.alpha_frame, text="Sélectionner l'image NB", command=self.select_alpha_image).grid(row=1, column=1, padx=10, pady=5, sticky="e")
        
        self.alpha_image_preview = ctk.CTkLabel(self.alpha_frame, text="")
        self.alpha_image_preview.grid(row=2, column=0, columnspan=2, pady=5)

        # --- Frame for Output Directory Selection ---
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.pack(pady=10, padx=20, fill="x")
        self.output_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.output_frame, text="Répertoire de sortie :", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, pady=5)
        self.output_dir_label = ctk.CTkLabel(self.output_frame, text="Aucun répertoire sélectionné", text_color="gray")
        self.output_dir_label.grid(row=1, column=0, padx=10, sticky="w")
        ctk.CTkButton(self.output_frame, text="Sélectionner le répertoire de sortie", command=self.select_output_directory).grid(row=1, column=1, padx=10, pady=5, sticky="e")

        # --- Process Button ---
        ctk.CTkButton(self, text="Fusionner les images", command=self.process_images, 
                      font=ctk.CTkFont(size=16, weight="bold"), 
                      fg_color="green", hover_color="darkgreen").pack(pady=20)
        
        # --- Output Image Preview ---
        self.output_preview_frame = ctk.CTkFrame(self)
        self.output_preview_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(self.output_preview_frame, text="Aperçu de l'image de sortie :", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        self.output_image_preview = ctk.CTkLabel(self.output_preview_frame, text="Aucune image traitée", text_color="gray")
        self.output_image_preview.pack(pady=5)


    def _load_and_display_image(self, file_path, label_widget):
        """Helper to load and display an image thumbnail."""
        if file_path and os.path.exists(file_path):
            try:
                img = Image.open(file_path)
                img.thumbnail((150, 150)) # Create a thumbnail
                img_tk = ImageTk.PhotoImage(img)
                label_widget.configure(image=img_tk, text="")
                label_widget.image = img_tk # Keep a reference!
            except Exception as e:
                label_widget.configure(image=None, text=f"Erreur de chargement: {e}", text_color="red")
        else:
            label_widget.configure(image=None, text="Aucun fichier sélectionné", text_color="gray")


    def select_base_image(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionner l'image de base",
            filetypes=[("Fichiers images", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"), ("Tous les fichiers", "*.*")]
        )
        if file_path:
            self.base_image_path = file_path
            self.base_path_label.configure(text=os.path.basename(file_path), text_color="white")
            self._load_and_display_image(file_path, self.base_image_preview)

    def select_alpha_image(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionner l'image Noir et Blanc (canal Alpha)",
            filetypes=[("Fichiers images", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"), ("Tous les fichiers", "*.*")]
        )
        if file_path:
            self.alpha_image_path = file_path
            self.alpha_path_label.configure(text=os.path.basename(file_path), text_color="white")
            self._load_and_display_image(file_path, self.alpha_image_preview)

    def select_output_directory(self):
        dir_path = filedialog.askdirectory(title="Sélectionner le répertoire de sortie")
        if dir_path:
            self.output_directory = dir_path
            self.output_dir_label.configure(text=dir_path, text_color="white")

    def process_images(self):
        if not self.base_image_path:
            messagebox.showwarning("Attention", "Veuillez sélectionner l'image de base.")
            return
        if not self.alpha_image_path:
            messagebox.showwarning("Attention", "Veuillez sélectionner l'image Noir et Blanc.")
            return
        if not self.output_directory:
            messagebox.showwarning("Attention", "Veuillez sélectionner le répertoire de sortie.")
            return

        output_filename = os.path.join(self.output_directory, "image_avec_canal_alpha.png")

        if apply_alpha_channel(self.base_image_path, self.alpha_image_path, output_filename):
            messagebox.showinfo("Succès", f"L'image a été traitée et sauvegardée sous :\n{output_filename}")
            self._load_and_display_image(output_filename, self.output_image_preview)
        else:
            self.output_image_preview.configure(image=None, text="Échec du traitement", text_color="red")


if __name__ == "__main__":
    app = ImageProcessorApp()
    app.mainloop()
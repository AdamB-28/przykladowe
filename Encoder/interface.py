import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from transcoding import CharVectorConverter

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_img = None
        self.title("RGB Image")
        self.iconbitmap("Encoder\\favicon.ico")
        self.to_encode = ""
        
        self.converter = CharVectorConverter()
        self.initialize_ui()

    def open_input_window(self):
        self.input_window = tk.Toplevel(self)
        self.input_window.title("Wpisz tekst do zakodowania")
        
        self.text_input = tk.Text(self.input_window, width=50, height=10)
        self.text_input.pack(pady=10)
        
        submit_button = tk.Button(self.input_window, text="Wyślij", command=self.submit_text)
        submit_button.pack()

    def submit_text(self):
        self.to_encode = self.text_input.get("1.0", tk.END).strip()
        self.input_window.destroy()
        self.encode_into_an_image()

    def encode_into_an_image(self):
        if self.current_img is not None:
            pixels = self.current_img.load()
            encoded_text = self.converter.sentence_to_vectors(self.to_encode)

            for x in range(self.current_img.width):
                for y in range(self.current_img.height):
                    if len(encoded_text) > 0:
                        current_pixel = pixels[x, y]
                        text_pixel = tuple(encoded_text.pop(0))
                        
                        # odejmowanie jesli wartosc przekroczy 255
                        new_pixel = tuple(min(255, max(0, current_pixel[i] + text_pixel[i] if current_pixel[i] + text_pixel[i] <= 255 else 255 - (current_pixel[i] + text_pixel[i] - 255))) for i in range(3))
                        
                        pixels[x, y] = new_pixel
                        print(current_pixel , new_pixel)
                    else:
                        break
            self.tk_image = ImageTk.PhotoImage(self.current_img)
            self.label.configure(image=self.tk_image)
            self.label.image = self.tk_image
        else:
            messagebox.showinfo("Wiadomość","Najpierw wybierz obraz")
    


    def decode_image(self):
        # Ask user to load the original image
        original_file_path = filedialog.askopenfilename(title="Wybierz pierwszy obraz")
        if not original_file_path:
            print("Original image not selected.")
            return

        # Load the original image
        self.original_img = Image.open(original_file_path)

        # Ask user to load the encoded image
        encoded_file_path = filedialog.askopenfilename(title="Wybierz drugi obraz")
        if not encoded_file_path:
            print("Encoded image not selected.")
            return

        # Load the encoded image
        self.encoded_img = Image.open(encoded_file_path)

        # Check if images have the same dimensions
        if self.original_img.size != self.encoded_img.size:
            messagebox.showinfo("Wiadomość","Rozmiary obrazów nie zgadzają się")
            return

        original_pixels = self.original_img.load()
        encoded_pixels = self.encoded_img.load()
        differences = []

        for x in range(self.original_img.width):
            for y in range(self.original_img.height):
                original_pixel = original_pixels[x, y]
                encoded_pixel = encoded_pixels[x, y]

                # Calculate the absolute difference per channel
                difference_pixel = tuple(abs(encoded_pixel[i] - original_pixel[i]) for i in range(3))
                differences.append(difference_pixel)

        # Assuming the converter can handle the differences to decode the message
        decoded_text = self.converter.vectors_to_sentence(differences)
        print(decoded_text)
        messagebox.showinfo("Odkodowana wiadmość", decoded_text)

    def initialize_ui(self):
        img = Image.new('RGB', (100, 100), color='white')
        self.tk_image = ImageTk.PhotoImage(img)        
        self.label = tk.Label(self, image=self.tk_image)
        self.label.pack()

        # Buttons
        self.save_as_button = tk.Button(self, text="Zapisz jako", command=self.save_image_as)
        self.save_as_button.pack()

        self.open_image_from_file_button = tk.Button(self, text="Otwórz", command=self.open_image)
        self.open_image_from_file_button.pack()

        self.open_image_from_file_button = tk.Button(self, text="Odkoduj", command=self.decode_image)
        self.open_image_from_file_button.pack()

        self.encode_file_button = tk.Button(self, text="Zakoduj", command=self.open_input_window)
        self.encode_file_button.pack()

    def save_image_as(self):
        if self.current_img is not None:
            # Prompt user for file path and file type to save the image
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                    filetypes=[("PNG files", "*.png")])
            if file_path:
                # Use the PIL Image save method to save the current image
                self.current_img.save(file_path)

    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.current_img = Image.open(file_path)
            self.tk_image = ImageTk.PhotoImage(self.current_img)
            self.label.configure(image=self.tk_image)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
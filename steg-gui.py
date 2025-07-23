import tkinter as tk                                                                               
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from stegano import lsb
import base64
import os

# === Welcome Screen class ===
class WelcomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome")
        self.root.geometry("400x200")
        self.root.resizable(False, False)

        label = tk.Label(root, text="Welcome to NR-ox033 Steg", font=("Arial", 16))
        label.pack(pady=30)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)

        start_btn = tk.Button(btn_frame, text="Start", width=10, command=self.start_app)
        start_btn.pack(side=tk.LEFT, padx=10)

        exit_btn = tk.Button(btn_frame, text="Exit", width=10, command=self.exit_app)
        exit_btn.pack(side=tk.LEFT, padx=10)

    def start_app(self):
        self.root.destroy()  # Close welcome window
        main_window = tk.Tk()
        app = SteganographyGUI(main_window)
        main_window.mainloop()

    def exit_app(self):
        self.root.destroy()

# === Main App GUI Class ===
class SteganographyGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Steganography Tool - GUI Version")
        self.master.geometry("800x600")

        self.tab_control = ttk.Notebook(master)

        self.tab_text = ttk.Frame(self.tab_control)
        self.tab_file = ttk.Frame(self.tab_control)
        self.tab_extract = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_text, text='Hide Text')
        self.tab_control.add(self.tab_file, text='Hide File')
        self.tab_control.add(self.tab_extract, text='Extract')
        self.tab_control.pack(expand=1, fill="both")

        self.setup_tab_text()
        self.setup_tab_file()
        self.setup_tab_extract()

    def setup_tab_text(self):
        tk.Label(self.tab_text, text="Input Image").pack()
        self.text_input_image = tk.Entry(self.tab_text, width=50)
        self.text_input_image.pack()
        tk.Button(self.tab_text, text="Browse", command=self.browse_text_input).pack()

        tk.Label(self.tab_text, text="Text to Hide").pack()
        self.text_to_hide = tk.Entry(self.tab_text, width=50)
        self.text_to_hide.pack()

        tk.Label(self.tab_text, text="Output Image").pack()
        self.text_output_image = tk.Entry(self.tab_text, width=50)
        self.text_output_image.pack()
        tk.Button(self.tab_text, text="Save As", command=self.save_text_output).pack()

        tk.Button(self.tab_text, text="Hide Text", command=self.hide_text).pack(pady=10)

    def setup_tab_file(self):
        tk.Label(self.tab_file, text="Input Image").pack()
        self.file_input_image = tk.Entry(self.tab_file, width=50)
        self.file_input_image.pack()
        tk.Button(self.tab_file, text="Browse", command=self.browse_file_input).pack()

        tk.Label(self.tab_file, text="File to Hide").pack()
        self.file_to_hide = tk.Entry(self.tab_file, width=50)
        self.file_to_hide.pack()
        tk.Button(self.tab_file, text="Browse", command=self.browse_file_to_hide).pack()

        tk.Label(self.tab_file, text="Output Image").pack()
        self.file_output_image = tk.Entry(self.tab_file, width=50)
        self.file_output_image.pack()
        tk.Button(self.tab_file, text="Save As", command=self.save_file_output).pack()

        tk.Button(self.tab_file, text="Hide File", command=self.hide_file).pack(pady=10)

    def setup_tab_extract(self):
        tk.Label(self.tab_extract, text="Image File").pack()
        self.extract_image = tk.Entry(self.tab_extract, width=50)
        self.extract_image.pack()
        tk.Button(self.tab_extract, text="Browse", command=self.browse_extract_image).pack()

        tk.Button(self.tab_extract, text="Extract Data", command=self.extract_data).pack(pady=10)
        self.result_text = tk.Text(self.tab_extract, height=10)
        self.result_text.pack(fill=tk.BOTH, expand=True)

    # ---------- Browse Methods ----------
    def browse_text_input(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
        if path:
            self.text_input_image.delete(0, tk.END)
            self.text_input_image.insert(0, path)

    def save_text_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if path:
            self.text_output_image.delete(0, tk.END)
            self.text_output_image.insert(0, path)

    def browse_file_input(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
        if path:
            self.file_input_image.delete(0, tk.END)
            self.file_input_image.insert(0, path)

    def save_file_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if path:
            self.file_output_image.delete(0, tk.END)
            self.file_output_image.insert(0, path)

    def browse_file_to_hide(self):
        path = filedialog.askopenfilename()
        if path:
            self.file_to_hide.delete(0, tk.END)
            self.file_to_hide.insert(0, path)

    def browse_extract_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
        if path:
            self.extract_image.delete(0, tk.END)
            self.extract_image.insert(0, path)

    # ---------- Functionality ----------
    def hide_text(self):
        input_img = self.text_input_image.get()
        output_img = self.text_output_image.get()
        message = self.text_to_hide.get()

        if not (input_img and output_img and message):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            encoded_message = base64.b64encode(message.encode()).decode()
            secret = lsb.hide(input_img, encoded_message)
            secret.save(output_img)
            messagebox.showinfo("Success", f"Text hidden successfully in: {output_img}")
            self.text_input_image.delete(0, tk.END)
            self.text_output_image.delete(0, tk.END)
            self.text_to_hide.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def hide_file(self):
        input_img = self.file_input_image.get()
        output_img = self.file_output_image.get()
        file_path = self.file_to_hide.get()

        if not (input_img and output_img and file_path):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            with open(file_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
            filename = os.path.basename(file_path)
            payload = f"FILE:{filename};DATA:{encoded}"
            secret = lsb.hide(input_img, payload)
            secret.save(output_img)
            messagebox.showinfo("Success", f"File hidden successfully in: {output_img}")
            self.file_input_image.delete(0, tk.END)
            self.file_output_image.delete(0, tk.END)
            self.file_to_hide.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_data(self):
        image_path = self.extract_image.get()
        if not image_path:
            messagebox.showerror("Error", "Please select an image file.")
            return
        try:
            data = lsb.reveal(image_path)
            if not data:
                self.result_text.insert(tk.END, "[-] No hidden data found.\n")
                return

            if data.startswith("FILE:"):
                try:
                    parts = data.split(";DATA:")
                    if len(parts) != 2:
                        raise ValueError("Invalid format for embedded file.")
                    filename_part = parts[0]
                    b64_content = parts[1]
                    filename = filename_part.replace("FILE:", "").strip()

                    # Save the base64 string into the file (not decoded)
                    with open(filename, "w") as f:
                        f.write(b64_content)

                    self.result_text.insert(tk.END, f"[+] Base64 content saved as: {filename}\n")
                except Exception as e:
                    self.result_text.insert(tk.END, f"[!] Failed to extract file: {e}\n")
            else:
                try:
                    decoded_text = base64.b64decode(data.encode()).decode()
                    self.result_text.insert(tk.END, f"[+] Hidden Text:\n{decoded_text}\n")
                except Exception:
                    self.result_text.insert(tk.END, f"[!] Invalid base64 text.\n{data}\n")

        except Exception as e:
            self.result_text.insert(tk.END, f"[!] Error extracting data: {e}\n")

# === Launch Welcome Screen ===
if __name__ == '__main__':
    welcome_root = tk.Tk()
    welcome_screen = WelcomeScreen(welcome_root)
    welcome_root.mainloop()

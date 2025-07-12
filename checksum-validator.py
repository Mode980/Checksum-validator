import hashlib
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD

# ----------------- Core Logic -----------------
def calculate_checksum(file_path, algorithm='sha256'):
    hash_func = getattr(hashlib, algorithm)()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        return None

def get_checksum_from_file(checksum_file):
    try:
        with open(checksum_file, 'r') as f:
            line = f.readline().strip()
            expected_checksum, filename = line.split()
            return expected_checksum, filename
    except Exception:
        return None, None

# ----------------- GUI App -----------------
class ChecksumVerifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Checksum Verifier")
        self.root.geometry("700x660")
        self.root.configure(bg="#121212")

        accent_color = "#00bcd4"  # Cyan Accent
        dark_bg = "#1f1f1f"
        light_text = "#ffffff"

        style = ttk.Style()
        style.theme_use("clam")

        # Custom dark theme with accent color
        style.configure("TLabel", background="#121212", foreground="#f0f0f0", font=("Segoe UI", 11))
        style.configure("TButton", background=accent_color, foreground="white", font=("Segoe UI", 10, "bold"), padding=10)
        style.map("TButton", background=[('active', '#0097a7')], foreground=[('active', 'white')])
        style.configure("TEntry", fieldbackground=dark_bg, foreground=light_text, padding=5, font=("Segoe UI", 10))

        style.configure("TCombobox",
                        fieldbackground=dark_bg,
                        background=dark_bg,
                        foreground=light_text,
                        selectbackground=dark_bg,
                        selectforeground=light_text,
                        arrowsize=15,
                        padding=5,
                        relief="flat",
                        bordercolor=accent_color)

        self.checksum_file_path = tk.StringVar()
        self.target_file_path = tk.StringVar()
        self.manual_checksum = tk.StringVar()
        self.selected_algorithm = tk.StringVar(value="auto")
        self.calculated_checksum = tk.StringVar()

        self.build_gui()
        self.setup_drag_and_drop()

    def build_gui(self):
        padding_y = 10

        ttk.Label(self.root, text="🎯 Select the File to Validate:").pack(pady=(padding_y, 5))
        ttk.Entry(self.root, textvariable=self.target_file_path, width=70).pack(pady=(0, 5))
        ttk.Button(self.root, text="Browse File", command=self.browse_target_file).pack(pady=padding_y)

        ttk.Label(self.root, text="📄 Checksum File (.sha256/.md5):").pack(pady=(padding_y, 5))
        ttk.Entry(self.root, textvariable=self.checksum_file_path, width=70).pack(pady=(0, 5))
        ttk.Button(self.root, text="Browse Checksum File", command=self.browse_checksum_file).pack(pady=padding_y)

        ttk.Label(self.root, text="✏️ Or Paste Checksum Directly:").pack(pady=(padding_y, 5))
        checksum_entry = ttk.Entry(self.root, textvariable=self.manual_checksum, width=70)
        checksum_entry.pack(pady=(0, padding_y))
        checksum_entry.configure(foreground="white")

        ttk.Label(self.root, text="🔧 Select Algorithm (or Auto):").pack(pady=(padding_y, 5))
        algo_dropdown = ttk.Combobox(self.root, textvariable=self.selected_algorithm,
                                     values=["auto", "sha256", "md5", "sha1"],
                                     state="readonly", width=30)
        # Removed problematic configure line that causes the app not to run
        # algo_dropdown.configure(font=("Segoe UI", 10), background="#1f1f1f", foreground="#ffffff")
        algo_dropdown.pack(pady=(0, padding_y))

        ttk.Button(self.root, text="✅ Verify Checksum", command=self.verify_checksum).pack(pady=20)

        self.result_label = ttk.Label(self.root, text="", font=("Segoe UI", 13, "bold"))
        self.result_label.pack(pady=10)

        self.calculated_label = ttk.Label(self.root, textvariable=self.calculated_checksum, font=("Segoe UI", 10))
        self.calculated_label.pack(pady=(5, 10))

        # Developer credit label in bottom-right
        dev_label = ttk.Label(self.root, text="Developed by Mohamed Elshazly", font=("Segoe UI", 9), anchor='e')
        dev_label.pack(side="bottom", anchor="se", padx=10, pady=5)

    def setup_drag_and_drop(self):
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_file_drop)

    def handle_file_drop(self, event):
        dropped_files = self.root.tk.splitlist(event.data)
        if dropped_files:
            self.target_file_path.set(dropped_files[0])

    def browse_checksum_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Checksum Files", "*.sha256 *.md5 *.sha1")])
        if file_path:
            self.checksum_file_path.set(file_path)

    def browse_target_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.target_file_path.set(file_path)

    def verify_checksum(self):
        file_path = self.target_file_path.get()
        checksum_file = self.checksum_file_path.get()
        manual_checksum = self.manual_checksum.get().strip()
        selected_algo = self.selected_algorithm.get()

        if not file_path:
            messagebox.showerror("Error", "Please select the file to validate.")
            return

        # Determine algorithm
        if selected_algo == "auto":
            if checksum_file.endswith('.sha256'):
                algorithm = 'sha256'
            elif checksum_file.endswith('.md5'):
                algorithm = 'md5'
            elif checksum_file.endswith('.sha1'):
                algorithm = 'sha1'
            elif manual_checksum:
                if len(manual_checksum) == 64:
                    algorithm = 'sha256'
                elif len(manual_checksum) == 40:
                    algorithm = 'sha1'
                elif len(manual_checksum) == 32:
                    algorithm = 'md5'
                else:
                    messagebox.showerror("Error", "Could not detect hash algorithm from checksum length.")
                    return
            else:
                messagebox.showerror("Error", "Please provide a valid checksum file or paste a checksum.")
                return
        else:
            algorithm = selected_algo

        if manual_checksum:
            expected_checksum = manual_checksum
        else:
            expected_checksum, _ = get_checksum_from_file(checksum_file)
            if not expected_checksum:
                messagebox.showerror("Error", "Invalid checksum file format.")
                return

        self.result_label.config(text=f"Verifying {os.path.basename(file_path)}...", foreground="orange")
        self.root.update()

        actual_checksum = calculate_checksum(file_path, algorithm)
        self.calculated_checksum.set(f"Calculated {algorithm.upper()} checksum:\n{actual_checksum}")

        if actual_checksum == expected_checksum.lower():
            self.result_label.config(text="✅ Checksum is VALID.", foreground="lime")
        else:
            self.result_label.config(text="❌ Checksum does NOT match.", foreground="red")

# ----------------- Run App -----------------
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ChecksumVerifierApp(root)
    root.mainloop()

# 🔐 Checksum Validator

A simple and elegant Python GUI application that verifies the integrity of files using SHA256, MD5, or SHA-1 checksums.

Developed with **Tkinter** and enhanced with **drag-and-drop**, algorithm auto-detection, and a clean dark theme UI.

---

## ✨ Features

* ✅ Verify checksum of any file using SHA256, MD5, or SHA-1
* 🧠 Auto-detect algorithm from checksum format or file extension
* 📄 Support for loading checksum from `.sha256`, `.md5`, `.sha1` files
* 📝 Paste checksum manually
* 🎨 Dark theme with Cyan accent and responsive layout
* 📂 Drag and drop support for easy file selection
* ⚙️ Exported as `.exe` for Windows using PyInstaller

---

## 🚀 Run It (Locally)

### Prerequisites

* Python 3.10+
* Install dependencies:

```bash
pip install tkinterdnd2
```

### Run the App

```bash
python checksum-validator.py
```

---

## 🛠️ Build an EXE

You can build the app as a portable Windows `.exe` file using **PyInstaller**:

```bash
pyinstaller --noconsole --onefile --icon=app_icon.ico --add-data ".venv\\Lib\\site-packages\\tkinterdnd2;tkinterdnd2" checksum-validator.py
```

Make sure the `.ico` file is in the same folder as your script.

---

## 📷 Screenshot

<img width="693" height="689" alt="image" src="https://github.com/user-attachments/assets/fe22781d-75fb-4701-a1ee-27935c8f4f36" />

---

## 📁 Project Structure

```
mode980/
│
├── checksum-validator.py        # Main script
├── app_icon.ico                 # Custom app icon (optional)
├── README.md                    # Project documentation
├── build/                       # PyInstaller build output
├── dist/                        # Final .exe file
└── .venv/                       # Virtual environment
```

---

## 👤 Developed by

**Mohamed Elshazly**
Cairo, Egypt 🇪🇬

> Proudly made with Python 💙


# Install Tesseract Engine

Mac
```
brew install tesseract
```

Linux
```
sudo apt update
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

Windows
```
You can download an installer from the UB Mannheim Tesseract GitHub page.

After installing Tesseract, you need to make sure it's in your system's PATH. You can test this by running tesseract --version in your terminal. If you see version information for Tesseract, then it's in your PATH. If you see an error message, then it's not in your PATH.

If Tesseract is not in your PATH after installation, you'll need to add it. The process for this varies depending on your operating system:
```

# ensure tesseract is in the path

Run this:
```
tesseract
```

if it does not work, add tesseract folder to the PATH

# pip install

```
pip install -r requirements.txt
```
# Run Main

```
python main.py
```
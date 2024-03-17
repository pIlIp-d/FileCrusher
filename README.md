# File Crusher
Compresses PDFs with PNG compression.

Tired of bumping against upload size limits? This tool is perfect to compress PDFs and PNGs by combining some of the best compression tools in one.
While it can be slow, it really crushes your filesize and helps you to conquer the relentless 5MB upload limit.

It works by splitting up a PDF into PNGs and compress these with advpng, pngcrush and pngquant. Then it combines them back into a PDF and applies a round of lossless pdf compression. Optionally it can apply OCR - Optical Character Recognition to make a scanned PDF searchable.

## Installation

### 1. Install the python library

```bash
pip install file-crusher
```

### 2. Install the Compression Tools

#### windows
already pre-installed in compressor_lib directory

#### Linux(ubuntu)

```bash
sudo apt install pngquant -y && sudo apt install advancecomp -y && sudo apt install pngcrush -y
```
and install wine for cpdfsqueeze
```bash
apt install wine -y
```

### 3. Install pytesseract for OCR

#### For Windows via GUI
Download and Install [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
Select Additional Languages that you want. (f.e German under Additional Language Data)

#### Linux
```bash
apt install tesseract-ocr
```

add additional language packs
```bash
apt install tesseract-ocr-<language-shortform> -y
```

example for german
```bash
apt install tesseract-ocr-deu -y
```

## Usage

```python3

```

## How it works


## Disclaimer

It's important to note that lossy compression results in loss of quality or data.
Therefore, it's always a good idea to test the output file to make sure it meets your requirements.

If you encounter any challenges while using the library or have suggestions for its improvement, I invite you to please create an issue. [https://github.com/pIlIp-d/FileCrusher/issues](https://github.com/pIlIp-d/FileCrusher/issues)

from pdf2image import convert_from_path
import pytesseract

def ocr_from_scanned_pdf(pdf_path: str) -> str:
    pages = convert_from_path(pdf_path)
    full_text = ''
    for page in pages:
        text = pytesseract.image_to_string(page, lang='spa')
        full_text += text + "\n\n"  # agrega un salto de línea entre páginas
    return full_text

if __name__ == '__main__':
    archivo_pdf = 'AQUÍVAELARCHIVOPDF.pdf'  # Ajusta nombre y ruta
    texto = ocr_from_scanned_pdf(archivo_pdf)
    print(texto)
    with open('texto_extraido.txt', 'w', encoding='utf-8') as f:
        f.write(texto)

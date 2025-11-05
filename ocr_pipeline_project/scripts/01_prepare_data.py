import os
from pdf2image import convert_from_path
from glob import glob

# --- Конфигурация путей ---
# Относительные пути от корня проекта (ocr_pipeline_project)
RAW_PDF_DIR = "../data/raw"
PROCESSED_DIR = "../data/processed"
IMAGE_DIR = os.path.join(PROCESSED_DIR, "images")

def prepare_images_from_pdfs():
    """
    Конвертирует все PDF из RAW_PDF_DIR в изображения в PROCESSED_DIR/images.
    """
    os.makedirs(IMAGE_DIR, exist_ok=True)
    
    pdf_files = glob(os.path.join(RAW_PDF_DIR, "*.pdf"))
    if not pdf_files:
        print(f"В папке {RAW_PDF_DIR} не найдено PDF файлов.")
        return

    print("Начинается конвертация PDF в изображения...")
    for pdf_path in pdf_files:
        pdf_name = os.path.basename(pdf_path).split('.')[0]
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            # Формат имени: {имя_pdf}_page_{номер}.png
            image_filename = f"{pdf_name}_page_{i+1:03}.png"
            image_path = os.path.join(IMAGE_DIR, image_filename)
            image.save(image_path, "PNG")
            print(f"Сохранено: {image_path}")

    print("\nКонвертация завершена.")

if __name__ == "__main__":
    prepare_images_from_pdfs()
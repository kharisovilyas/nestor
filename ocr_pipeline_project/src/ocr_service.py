import numpy as np
from paddleocr import PaddleOCR
from pdf2image import convert_from_path

class OCRService:
    """
    Класс для извлечения текста из PDF-файлов с использованием PaddleOCR.
    Поддерживает как стандартные, так и дообученные модели.
    """
    def __init__(self, recognition_model_path: str = None):
        """
        Инициализирует модель PaddleOCR.

        Args:
            recognition_model_path (str, optional): 
                Путь к директории с дообученной моделью распознавания.
                Например: '../PaddleOCR/output/cyrillic_tuned_recognizer/'.
                Если None, используется стандартная русская модель.
        """
        lang = 'ru'
        
        if recognition_model_path:
            print(f"[*] Инициализация с дообученной моделью из: {recognition_model_path}")
        else:
            print("[*] Инициализация со стандартной русской моделью.")

        # use_angle_cls=True помогает модели правильно определять ориентацию текста
        # rec_model_dir - ключевой параметр для загрузки кастомной модели
        self.ocr_model = PaddleOCR(
            use_angle_cls=True,
            lang=lang,
            rec_model_dir=recognition_model_path
        )

    def extract_text(self, pdf_path: str) -> dict:
        """
        Извлекает текст из PDF-файла, возвращая результат в виде словаря по страницам.

        Args:
            pdf_path (str): Путь к PDF-файлу.

        Returns:
            dict: Словарь, где ключ - номер страницы ('page_1', 'page_2', ...),
                  а значение - распознанный текст на этой странице.
        """
        try:
            # Конвертируем PDF в список изображений (по одному на страницу)
            images = convert_from_path(pdf_path)
        except Exception as e:
            # Выдаем понятную ошибку, если Poppler не установлен или файл поврежден
            raise IOError(f"Ошибка при конвертации PDF '{pdf_path}'. Убедитесь, что Poppler установлен и файл не поврежден. Детали: {e}")
        
        results = {}
        print(f"[*] Найдено страниц: {len(images)}. Начинаю распознавание...")

        for i, image in enumerate(images):
            page_num = i + 1
            print(f"    - Обработка страницы {page_num}...")
            
            # Конвертируем изображение в формат, понятный для PaddleOCR
            image_np = np.array(image)
            
            # Запускаем процесс распознавания
            result = self.ocr_model.ocr(image_np, cls=True)
            
            page_text = ""
            # Результат приходит в виде сложной структуры, извлекаем только текст
            if result and result[0]:
                texts = [line[1][0] for line in result[0]]
                page_text = "\n".join(texts)
            
            results[f'page_{page_num}'] = page_text
            
        return results
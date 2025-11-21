import argparse
import os
import sys
import time

# Убедимся, что Python видит нашу папку src, где лежит PDFTextExtractor
# Это делает скрипт запускаемым из любого места
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from pdf_extractor import PDFTextExtractor

# --- КОНФИГУРАЦИЯ ПО УМОЛЧАНИЮ ---
# Путь к нашей дообученной модели. Он относителен от папки ocr_pipeline_project
DEFAULT_MODEL_DIR = "../PaddleOCR/output/cyrillic_tuned_recognizer/"


def create_argument_parser():
    """
    Создает и настраивает парсер аргументов командной строки.
    """
    parser = argparse.ArgumentParser(
        description="Консольное приложение для распознавания текста в PDF-файлах.",
        formatter_class=argparse.RawTextHelpFormatter  # Для красивого отображения help
    )
    
    parser.add_argument(
        "pdf_path",
        type=str,
        help="Путь к исходному PDF-файлу для распознавания."
    )
    
    parser.add_argument(
        "-m", "--model_dir",
        type=str,
        default=DEFAULT_MODEL_DIR,
        help="Путь к папке с дообученной моделью распознавания.\n"
             f"(по умолчанию: {DEFAULT_MODEL_DIR})"
    )
    
    parser.add_argument(
        "--use_default_model",
        action="store_true", # Создает флаг, который не требует значения (просто --use_default_model)
        help="Использовать стандартную модель PaddleOCR вместо дообученной."
    )

    parser.add_argument(
        "-o", "--output_path",
        type=str,
        default=None,
        help="Путь к текстовому файлу для сохранения результата.\n"
             "(по умолчанию: вывод в консоль)"
    )

    return parser


def main():
    """
    Основная логика приложения.
    """
    parser = create_argument_parser()
    args = parser.parse_args()

    # --- 1. Проверка входных данных ---
    if not os.path.exists(args.pdf_path):
        print(f"[!] Ошибка: PDF-файл не найден по пути: {args.pdf_path}")
        sys.exit(1)

    model_path_to_load = None
    if args.use_default_model:
        print("[*] Режим: используется стандартная модель PaddleOCR.")
    else:
        if not os.path.exists(args.model_dir):
            print(f"[!] Ошибка: Папка с дообученной моделью не найдена: {args.model_dir}")
            print("[!] Совет: Убедитесь, что вы провели обучение, или используйте флаг --use_default_model.")
            sys.exit(1)
        model_path_to_load = args.model_dir
        print(f"[*] Режим: используется дообученная модель из '{model_path_to_load}'.")

    # --- 2. Инициализация и запуск OCR ---
    try:
        print("\n[*] Загрузка OCR модели... Это может занять некоторое время.")
        start_time = time.time()
        
        extractor = PDFTextExtractor(recognition_model_path=model_path_to_load)
        
        load_time = time.time() - start_time
        print(f"[+] Модель успешно загружена за {load_time:.2f} сек.")

        print(f"\n[*] Начинается обработка файла: {os.path.basename(args.pdf_path)}...")
        start_time = time.time()
        
        results = extractor.extract_text(args.pdf_path)
        
        process_time = time.time() - start_time
        print(f"[+] Файл обработан за {process_time:.2f} сек.")
        
        # Объединяем текст со всех страниц
        full_text = "\n\n".join(results.values())

    except Exception as e:
        print(f"\n[!] Произошла критическая ошибка во время обработки: {e}")
        sys.exit(1)

    # --- 3. Вывод результата ---
    if args.output_path:
        try:
            with open(args.output_path, 'w', encoding='utf-8') as f:
                f.write(full_text)
            print(f"\n[+] Результат успешно сохранен в файл: {args.output_path}")
        except Exception as e:
            print(f"\n[!] Не удалось сохранить результат в файл: {e}")
    else:
        print("\n" + "="*20 + " РЕЗУЛЬТАТ РАСПОЗНАВАНИЯ " + "="*20)
        print(full_text)
        print("="*65)


if __name__ == "__main__":
    main()
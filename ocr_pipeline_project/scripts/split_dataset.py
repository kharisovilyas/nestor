import os
import random

# --- Конфигурация ---
# Пути относительные от корня проекта (ocr_pipeline_project)
PROCESSED_DIR = "../data/processed"
SOURCE_FILE = os.path.join(PROCESSED_DIR, "all_labels.txt")
TRAIN_FILE = os.path.join(PROCESSED_DIR, "train_labels.txt")
EVAL_FILE = os.path.join(PROCESSED_DIR, "eval_labels.txt")

# Пропорция разделения: 80% данных на обучение, 20% на оценку
TRAIN_RATIO = 0.8

def split_dataset():
    """
    Читает исходный файл с метками, перемешивает его и разделяет
    на обучающий (train) и оценочный (eval) наборы.
    """
    print(f"[*] Читаем исходный файл: {SOURCE_FILE}")
    try:
        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Ошибка: Файл {SOURCE_FILE} не найден!")
        print("[!] Пожалуйста, создайте его и заполните всеми вашими данными.")
        return

    if not lines:
        print("[!] Ошибка: Исходный файл пуст.")
        return

    # Перемешиваем строки в случайном порядке — это очень важный шаг!
    random.shuffle(lines)
    
    # Определяем точку разделения
    split_index = int(len(lines) * TRAIN_RATIO)
    
    train_data = lines[:split_index]
    eval_data = lines[split_index:]
    
    print(f"[*] Всего строк: {len(lines)}")
    print(f"[*] Строк для обучения (train): {len(train_data)}")
    print(f"[*] Строк для оценки (eval): {len(eval_data)}")
    
    # Запись обучающего набора
    try:
        with open(TRAIN_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(train_data))
        print(f"[+] Файл '{TRAIN_FILE}' успешно создан.")
    except Exception as e:
        print(f"[!] Не удалось записать файл {TRAIN_FILE}: {e}")

    # Запись оценочного набора
    try:
        with open(EVAL_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(eval_data))
        print(f"[+] Файл '{EVAL_FILE}' успешно создан.")
    except Exception as e:
        print(f"[!] Не удалось записать файл {EVAL_FILE}: {e}")


if __name__ == "__main__":
    split_dataset()
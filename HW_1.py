import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

def copy_file(src, dst):
    """Копіює файл з src до dst, створюючи цільову директорію, якщо її ще не існує."""
    try:
        if not os.path.exists(dst):
            os.makedirs(dst)  # Створює цільову директорію, якщо вона ще не існує
        shutil.copy2(src, dst)  # Копіює файл з збереженням метаданих
        print(f"Copied {src} to {dst}")
    except Exception as e:
        print(f"Failed to copy {src} to {dst}: {e}")

def process_directory(src_dir, dst_dir):
    """Рекурсивно обходить всі піддиректорії src_dir і копіює файли в dst_dir з розподілом за розширеннями."""
    with ThreadPoolExecutor() as executor:
        futures = []
        for root, _, files in os.walk(src_dir):
            for file in files:
                file_path = os.path.join(root, file)  # Отримує повний шлях до файлу
                extension = file.split('.')[-1]  # Витягує розширення файлу
                target_dir = os.path.join(dst_dir, extension)  # Визначає цільову директорію на основі розширення
                futures.append(executor.submit(copy_file, file_path, target_dir))  # Додає завдання копіювання до пулу потоків
        
        # Обробка результатів виконання потоків по мірі їх завершення
        for future in as_completed(futures):
            try:
                future.result()  # Цей виклик підіймає виключення, якщо воно відбулося в потоці
            except Exception as e:
                print(f"Error occurred: {e}")

def main():
    """Основна функція, яка обробляє аргументи командного рядка і запускає процес обробки директорії."""
    if len(sys.argv) < 2:
        print("Usage: python script.py <source_directory> [destination_directory]")
        sys.exit(1)

    src_dir = sys.argv[1]
    dst_dir = sys.argv[2] if len(sys.argv) > 2 else 'dist'

    if not os.path.exists(src_dir):
        print(f"Source directory {src_dir} does not exist")
        sys.exit(1)

    process_directory(src_dir, dst_dir)
    print(f"Files have been successfully copied to {dst_dir}")

if __name__ == '__main__':
    main()

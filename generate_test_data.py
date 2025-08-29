import os
from pathlib import Path

def create_test_files():
    """
    Створює папки 'source_files' і 'output_folder', а також 
    декілька тестових файлів у 'source_files' і файл requirements.txt.
    """
    # Визначення шляхів
    source_dir = Path("source_files")
    output_dir = Path("output_folder")
    requirements_file = Path("requirements.txt")

    # Створення папок
    print(f"Створення папок: {source_dir} та {output_dir}")
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Список файлів для створення
    files_to_create = {
        "text_files": ["document1.txt", "notes.txt"],
        "images": ["photo.jpg", "screenshot.png"],
        "code": ["script.py", "utility.js"],
        "other": ["data.csv", "archive.zip"],
        "no_extension": ["file_without_ext"],
    }

    # Створення файлів
    print("Створення тестових файлів...")
    for folder, file_list in files_to_create.items():
        sub_folder = source_dir / folder
        os.makedirs(sub_folder, exist_ok=True)
        for filename in file_list:
            file_path = sub_folder / filename
            with open(file_path, 'w') as f:
                f.write(f"Це тестовий файл: {filename}\n")
            print(f"Створено: {file_path}")

    # Створення файлу requirements.txt
    print(f"\nСтворення файлу: {requirements_file}")
    with open(requirements_file, 'w') as f:
        f.write("aiofiles\n")
        f.write("matplotlib\n")
        f.write("requests\n")
        
    print("Генерацію файлів завершено успішно.")

if __name__ == "__main__":
    create_test_files()

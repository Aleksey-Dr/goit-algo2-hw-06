import asyncio
import aiofiles
import os
import argparse
import logging
from pathlib import Path

# Налаштування логування
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

async def read_folder(source_folder: Path, output_folder: Path):
    """
    Асинхронно рекурсивно читає файли у вихідній папці та запускає копіювання.
    """
    tasks = []
    try:
        # Використання os.scandir() та run_in_executor для асинхронного сканування
        loop = asyncio.get_running_loop()
        entries = await loop.run_in_executor(None, os.scandir, source_folder)
        
        for entry in entries:
            if entry.is_file():
                tasks.append(asyncio.create_task(copy_file(Path(entry.path), output_folder)))
            elif entry.is_dir():
                tasks.append(asyncio.create_task(read_folder(Path(entry.path), output_folder)))
    except FileNotFoundError:
        logging.error(f"Вихідна папка не знайдена: {source_folder}")
        return
    except Exception as e:
        logging.error(f"Виникла помилка під час сканування папки {source_folder}: {e}")
        return
    
    if tasks:
        await asyncio.gather(*tasks)

async def copy_file(file_path: Path, output_folder: Path):
    """
    Асинхронно копіює файл у відповідну підпапку на основі його розширення.
    """
    extension = file_path.suffix.lstrip('.')
    if not extension:
        extension = "no_extension"
    
    destination_dir = output_folder / extension
    
    try:
        # Використання os.makedirs, бо aiofiles не має асинхронної версії
        os.makedirs(destination_dir, exist_ok=True)
        destination_path = destination_dir / file_path.name
        
        async with aiofiles.open(file_path, 'rb') as src_file:
            async with aiofiles.open(destination_path, 'wb') as dst_file:
                while True:
                    # Читання та запис блоками для ефективності
                    chunk = await src_file.read(4096)
                    if not chunk:
                        break
                    await dst_file.write(chunk)
        print(f"Файл скопійовано: {file_path.name} -> {destination_dir}")

    except Exception as e:
    # Явно перевіряємо, що помилка не пов'язана з відсутністю os в aiofiles.
        if "module 'aiofiles' has no attribute 'os'" in str(e):
            logging.error(f"Критична помилка: використовується застаріла версія aiofiles або неправильний імпорт.")
        else:
            logging.error(f"Помилка при копіюванні файлу {file_path}: {e}")

def main():
    """
    Основна функція для обробки аргументів та запуску асинхронного сортування.
    """
    parser = argparse.ArgumentParser(description="Асинхронний сортувальник файлів.")
    parser.add_argument("-s", "--source", type=str, required=True, help="Шлях до вихідної папки.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Шлях до цільової папки.")
    
    args = parser.parse_args()
    
    source_folder = Path(args.source)
    output_folder = Path(args.output)

    # Перевірка існування вихідної папки
    if not source_folder.exists() or not source_folder.is_dir():
        logging.error(f"Вихідна папка '{source_folder}' не існує або не є директорією.")
        return
    
    # Запуск асинхронного сортування
    asyncio.run(read_folder(source_folder, output_folder))

if __name__ == "__main__":
    main()

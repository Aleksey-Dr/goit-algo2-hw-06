import concurrent.futures
import re
import requests
from collections import defaultdict, Counter
import matplotlib.pyplot as plt

def download_text(url: str) -> str:
    """
    Завантажує текст із заданої URL-адреси.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Викликає HTTPError для поганих відповідей
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Помилка при завантаженні тексту: {e}")
        return ""

def mapper(text_chunk: str) -> Counter:
    """
    Функція Map: обробляє фрагмент тексту та підраховує слова.
    """
    # Розбиває текст на слова, ігноруючи пунктуацію та перетворюючи на нижній регістр
    words = re.findall(r'\b\w+\b', text_chunk.lower())
    return Counter(words)

def reducer(word_counts: list[Counter]) -> Counter:
    """
    Функція Reduce: об'єднує результати з усіх маперів.
    """
    total_counts = Counter()
    for counts in word_counts:
        total_counts.update(counts)
    return total_counts

def visualize_top_words(word_counts: Counter, top_n: int = 10):
    """
    Візуалізує топ-слова з найвищою частотою використання.
    """
    top_words = word_counts.most_common(top_n)
    
    if not top_words:
        print("Немає даних для візуалізації.")
        return
        
    words, counts = zip(*top_words)
    
    plt.style.use('seaborn-v0_8-whitegrid')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Створення горизонтальної стовпчастої діаграми
    bars = ax.barh(words, counts, color='skyblue')
    
    # Додавання підписів
    ax.set_title(f'Топ {top_n} найбільш вживаних слів', fontsize=16, pad=20)
    ax.set_xlabel('Частота', fontsize=12)
    ax.set_ylabel('Слова', fontsize=12)
    
    # Інвертування осі Y, щоб найпопулярніше слово було зверху
    ax.invert_yaxis()
    
    # Додавання значень на стовпці
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 50, bar.get_y() + bar.get_height()/2, 
                 f'{int(width)}', ha='left', va='center')
                 
    plt.tight_layout()
    plt.show()

def main():
    """
    Основна функція для виконання аналізу тексту.
    """
    # Використовуйте будь-яку URL, що містить багато тексту.
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"  # Наприклад, "Гордість і упередження"
    
    text = download_text(url)
    if not text:
        return
        
    # Розбиття тексту на фрагменти для багатопотокової обробки
    num_threads = 4
    text_chunks = [text[i::num_threads] for i in range(num_threads)]
    
    # Використання багатопотоковості з ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Map: застосування mapper до кожного фрагменту
        mapped_results = list(executor.map(mapper, text_chunks))
    
    # Reduce: об'єднання результатів
    final_counts = reducer(mapped_results)
    
    # Візуалізація результатів
    visualize_top_words(final_counts, top_n=10)

if __name__ == "__main__":
    main()
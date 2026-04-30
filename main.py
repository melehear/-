"""
Менеджер цитат - управляет хранением цитат, историей и фильтрацией
"""

import json
import random
from datetime import datetime
from typing import List, Dict, Optional

DATA_FILE = "books_data.json"

class QuoteManager:
    """Управляет операциями с цитатами и историей"""
    
    def __init__(self, quotes_file="quotes.json", history_file="history.json"):
        self.quotes_file = quotes_file
        self.history_file = history_file
        self.quotes = []
        self.history = []
        self.load_quotes()
        self.load_history()
    
    def load_quotes(self):
        """Загружает предопределённые цитаты из JSON-файла"""
        try:
            with open(self.quotes_file, 'r', encoding='utf-8') as f:
                self.quotes = json.load(f)
        except FileNotFoundError:
            # Цитаты по умолчанию, если файл не существует
            self.quotes = [
                {"text": "Будь тем изменением, которое хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "Вдохновение"},
                {"text": "Единственный предел — это твоё воображение.", "author": "Неизвестен", "topic": "Мотивация"},
                {"text": "Оставайтесь голодными, оставайтесь безрассудными.", "author": "Стив Джобс", "topic": "Успех"},
                {"text": "Быть или не быть — вот в чём вопрос.", "author": "Уильям Шекспир", "topic": "Философия"},
                {"text": "Я мыслю, следовательно, я существую.", "author": "Рене Декарт", "topic": "Философия"},
                {"text": "Будущее принадлежит тем, кто верит в красоту своей мечты.", "author": "Элеонора Рузвельт", "topic": "Вдохновение"},
                {"text": "Неважно, как медленно ты идёшь, главное — не останавливаться.", "author": "Конфуций", "topic": "Мотивация"},
                {"text": "Успех — это не окончательно, неудача — не фатальна: важна лишь смелость продолжать.", "author": "Уинстон Черчилль", "topic": "Успех"},
                {"text": "Жизнь — это то, что происходит с тобой, пока ты строишь другие планы.", "author": "Джон Леннон", "topic": "Жизнь"},
                {"text": "Единственный способ делать великую работу — любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "Карьера"},
                {"text": "Счастье — это не нечто готовое. Оно приходит от твоих собственных действий.", "author": "Далай-лама", "topic": "Счастье"},
                {"text": "В середине трудностей кроется возможность.", "author": "Альберт Эйнштейн", "topic": "Возможность"},
                {"text": "То, что нас не убивает, делает нас сильнее.", "author": "Фридрих Ницше", "topic": "Сила"},
                {"text": "Лучшее время посадить дерево было 20 лет назад. Следующее лучшее время — сейчас.", "author": "Китайская пословица", "topic": "Мотивация"},
                {"text": "Твоё время ограничено, не трать его, проживая чужую жизнь.", "author": "Стив Джобс", "topic": "Успех"}
            ]
            self.save_quotes()
    
    def save_quotes(self):
        """Сохраняет цитаты в JSON-файл"""
        with open(self.quotes_file, 'w', encoding='utf-8') as f:
            json.dump(self.quotes, f, ensure_ascii=False, indent=2)
    
    def load_history(self):
        """Загружает историю из JSON-файла"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []
    
    def save_history(self):
        """Сохраняет историю в JSON-файл"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add_quote(self, text: str, author: str, topic: str) -> bool:
        """Добавляет новую цитату с проверкой"""
        # Проверка ввода
        if not text or not text.strip():
            return False
        if not author or not author.strip():
            return False
        if not topic or not topic.strip():
            return False
        
        # Добавление цитаты
        self.quotes.append({
            "text": text.strip(),
            "author": author.strip(),
            "topic": topic.strip()
        })
        self.save_quotes()
        return True
    
    def get_random_quote(self) -> Dict:
        """Возвращает случайную цитату"""
        if not self.quotes:
            return {"text": "Нет доступных цитат!", "author": "Система", "topic": "Ошибка"}
        return random.choice(self.quotes)
    
    def add_to_history(self, quote: Dict):
        """Добавляет цитату в историю с отметкой времени"""
        history_entry = {
            "text": quote["text"],
            "author": quote["author"],
            "topic": quote["topic"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(history_entry)
        self.save_history()
    
    def get_all_authors(self) -> List[str]:
        """Возвращает список уникальных авторов"""
        return sorted(list(set(q["author"] for q in self.quotes)))
    
    def get_all_topics(self) -> List[str]:
        """Возвращает список уникальных тем"""
        return sorted(list(set(q["topic"] for q in self.quotes)))
    
    def filter_quotes(self, author: Optional[str] = None, topic: Optional[str] = None) -> List[Dict]:
        """Фильтрует цитаты по автору и/или теме"""
        filtered = self.quotes.copy()
        
        if author and author != "Все":
            filtered = [q for q in filtered if q["author"] == author]
        
        if topic and topic != "Все":
            filtered = [q for q in filtered if q["topic"] == topic]
        
        return filtered
    
    def get_filtered_random_quote(self, author: Optional[str] = None, topic: Optional[str] = None) -> Optional[Dict]:
        """Возвращает случайную цитату из отфильтрованного списка"""
        filtered = self.filter_quotes(author, topic)
        if not filtered:
            return None
        return random.choice(filtered)
    
    def clear_history(self):
        """Очищает всю историю"""
        self.history = []
        self.save_history()
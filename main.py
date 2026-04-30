"""
Quote Manager - Handles quotes storage, history, and filtering
Author: Иван Иванов
"""

import json
import random
from datetime import datetime
from typing import List, Dict, Optional

class QuoteManager:
    """Manages quotes and history operations"""
    
    def __init__(self, quotes_file="quotes.json", history_file="history.json"):
        self.quotes_file = quotes_file
        self.history_file = history_file
        self.quotes = []
        self.history = []
        self.load_quotes()
        self.load_history()
    
    def load_quotes(self):
        """Load predefined quotes from JSON file"""
        try:
            with open(self.quotes_file, 'r', encoding='utf-8') as f:
                loaded_quotes = json.load(f)
                if loaded_quotes:
                    self.quotes = loaded_quotes
                else:
                    self._load_default_quotes()
        except FileNotFoundError:
            self._load_default_quotes()
        except json.JSONDecodeError:
            print("Ошибка чтения quotes.json, загружаются цитаты по умолчанию")
            self._load_default_quotes()
    
    def _load_default_quotes(self):
        """Load default quotes"""
        self.quotes = [
            {"text": "Будь тем изменением, которое хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "Вдохновение"},
            {"text": "Единственный предел — это твоё воображение.", "author": "Неизвестен", "topic": "Мотивация"},
            {"text": "Оставайтесь голодными, оставайтесь безрассудными.", "author": "Стив Джобс", "topic": "Успех"},
            {"text": "Быть или не быть — вот в чём вопрос.", "author": "Уильям Шекспир", "topic": "Философия"},
            {"text": "Я мыслю, следовательно, я существую.", "author": "Рене Декарт", "topic": "Философия"},
            {"text": "Будущее принадлежит тем, кто верит в красоту своей мечты.", "author": "Элеонора Рузвельт", "topic": "Вдохновение"},
            {"text": "Неважно, как медленно ты идёшь, главное — не останавливаться.", "author": "Конфуций", "topic": "Мотивация"},
            {"text": "Успех — это не окончательно, неудача — не фатальна: важна лишь смелость продолжать.", "author": "Уинстон Черчилль", "topic": "Успех"},
            {"text": "Жизнь — это то, что происходит с тобой, пока ты строишь другие планы.", "author": "Джон Леннон", "topic": "Жизнь"}
        ]
        self.save_quotes()
    
    def save_quotes(self):
        """Save quotes to JSON file"""
        try:
            with open(self.quotes_file, 'w', encoding='utf-8') as f:
                json.dump(self.quotes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения quotes.json: {e}")
    
    def load_history(self):
        """Load history from JSON file"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []
        except json.JSONDecodeError:
            print("Ошибка чтения history.json, создаётся новая история")
            self.history = []
    
    def save_history(self):
        """Save history to JSON file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения history.json: {e}")
    
    def add_quote(self, text: str, author: str, topic: str) -> tuple:
        """
        Add a new quote with validation
        Returns: (success: bool, error_message: str)
        """
        # Проверка на пустые строки
        if not text or not text.strip():
            return False, "Текст цитаты не может быть пустым!"
        if not author or not author.strip():
            return False, "Имя автора не может быть пустым!"
        if not topic or not topic.strip():
            return False, "Тема не может быть пустой!"
        
        # Проверка на минимальную длину
        if len(text.strip()) < 5:
            return False, "Текст цитаты должен содержать минимум 5 символов!"
        
        # Добавление цитаты
        self.quotes.append({
            "text": text.strip(),
            "author": author.strip(),
            "topic": topic.strip()
        })
        self.save_quotes()
        return True, "Цитата успешно добавлена!"
    
    def get_random_quote(self) -> Dict:
        """Get a random quote"""
        if not self.quotes:
            return {"text": "Нет доступных цитат! Добавьте новую цитату.", "author": "Система", "topic": "Информация"}
        return random.choice(self.quotes)
    
    def add_to_history(self, quote: Dict):
        """Add quote to history with timestamp"""
        history_entry = {
            "text": quote["text"],
            "author": quote["author"],
            "topic": quote["topic"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(history_entry)
        self.save_history()
    
    def get_all_authors(self) -> List[str]:
        """Get list of unique authors"""
        return sorted(list(set(q["author"] for q in self.quotes)))
    
    def get_all_topics(self) -> List[str]:
        """Get list of unique topics"""
        return sorted(list(set(q["topic"] for q in self.quotes)))
    
    def get_quotes_by_filter(self, author: Optional[str] = None, topic: Optional[str] = None) -> List[Dict]:
        """Get all quotes by filter (not random)"""
        filtered = self.quotes.copy()
        
        if author and author != "Все":
            filtered = [q for q in filtered if q["author"] == author]
        
        if topic and topic != "Все":
            filtered = [q for q in filtered if q["topic"] == topic]
        
        return filtered
    
    def get_filtered_random_quote(self, author: Optional[str] = None, topic: Optional[str] = None) -> Optional[Dict]:
        """Get random quote from filtered list"""
        filtered = self.get_quotes_by_filter(author, topic)
        if not filtered:
            return None
        return random.choice(filtered)
    
    def get_history_by_filter(self, author: Optional[str] = None, topic: Optional[str] = None) -> List[Dict]:
        """Filter history by author and/or topic"""
        if (not author or author == "Все") and (not topic or topic == "Все"):
            return self.history.copy()
        
        filtered = self.history.copy()
        
        if author and author != "Все":
            filtered = [q for q in filtered if q["author"] == author]
        
        if topic and topic != "Все":
            filtered = [q for q in filtered if q["topic"] == topic]
        
        return filtered
    
    def clear_history(self):
        """Clear all history"""
        self.history = []
        self.save_history()
        return True
    
    def delete_quote(self, index: int) -> bool:
        """Delete a quote by index"""
        if 0 <= index < len(self.quotes):
            self.quotes.pop(index)
            self.save_quotes()
            return True
        return False
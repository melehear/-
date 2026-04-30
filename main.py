"""
Quote Manager - Handles quotes storage, history, and filtering
Author: Иван Иванов
"""

import json
import random
from datetime import datetime
from typing import List, Dict, Optional

DATA_FILE = "books_data.json"

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
        """
GUI Module - Provides the graphical user interface
Author: Иван Иванов
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from quote_manager import QuoteManager

class QuoteApp:
    """Main application class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.quote_manager = QuoteManager()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        self.root.title("Random Quote Generator v2.0")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container with notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Quote Generator
        self.generator_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.generator_frame, text="🎲 Генератор цитат")
        
        # Tab 2: All Quotes
        self.quotes_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.quotes_frame, text="📚 Все цитаты")
        
        # Tab 3: Add Quote
        self.add_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_frame, text="➕ Добавить цитату")
        
        # Tab 4: History
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="📜 История")
        
        # Setup each tab
        self.setup_generator_tab()
        self.setup_quotes_tab()
        self.setup_add_tab()
        self.setup_history_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе. Используйте вкладки для навигации.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initial refresh
        self.refresh_filters()
    
    def setup_generator_tab(self):
        """Setup the quote generator tab"""
        # Main frame
        main_frame = ttk.Frame(self.generator_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Filters frame
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтры", padding="10")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Author filter
        ttk.Label(filter_frame, text="Автор:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.gen_author_var = tk.StringVar(value="Все")
        self.gen_author_combo = ttk.Combobox(filter_frame, textvariable=self.gen_author_var, width=30)
        self.gen_author_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Topic filter
        ttk.Label(filter_frame, text="Тема:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.gen_topic_var = tk.StringVar(value="Все")
        self.gen_topic_combo = ttk.Combobox(filter_frame, textvariable=self.gen_topic_var, width=30)
        self.gen_topic_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Refresh filters button
        refresh_btn = ttk.Button(filter_frame, text="🔄 Обновить фильтры", command=self.refresh_filters)
        refresh_btn.grid(row=0, column=2, rowspan=2, padx=20, pady=5)
        
        # Quote display frame
        quote_frame = ttk.LabelFrame(main_frame, text="Случайная цитата", padding="10")
        quote_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.quote_text = scrolledtext.ScrolledText(quote_frame, height=8, wrap=tk.WORD, 
                                                      font=('Arial', 12), state='disabled')
        self.quote_text.pack(fill=tk.BOTH, expand=True)
        
        # Generate button
        generate_btn = ttk.Button(main_frame, text="🎲 Сгенерировать случайную цитату", 
                                 command=self.generate_quote)
        generate_btn.pack(pady=10)
    
    def setup_quotes_tab(self):
        """Setup the all quotes tab with filtering"""
        # Main frame
        main_frame = ttk.Frame(self.quotes_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Filters frame
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация цитат", padding="10")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Author filter
        ttk.Label(filter_frame, text="Автор:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.quotes_author_var = tk.StringVar(value="Все")
        self.quotes_author_combo = ttk.Combobox(filter_frame, textvariable=self.quotes_author_var, width=30)
        self.quotes_author_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Topic filter
        ttk.Label(filter_frame, text="Тема:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.quotes_topic_var = tk.StringVar(value="Все")
        self.quotes_topic_combo = ttk.Combobox(filter_frame, textvariable=self.quotes_topic_var, width=30)
        self.quotes_topic_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Apply filter button
        apply_filter_btn = ttk.Button(filter_frame, text="🔍 Применить фильтр", 
                                     command=self.display_filtered_quotes)
        apply_filter_btn.grid(row=0, column=2, rowspan=2, padx=20, pady=5)
        
        # Quotes display
        quotes_display_frame = ttk.LabelFrame(main_frame, text="Список цитат", padding="10")
        quotes_display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for quotes
        columns = ("ID", "Цитата", "Автор", "Тема")
        self.quotes_tree = ttk.Treeview(quotes_display_frame, columns=columns, show="headings", height=15)
        
        self.quotes_tree.heading("ID", text="№")
        self.quotes_tree.heading("Цитата", text="Цитата")
        self.quotes_tree.heading("Автор", text="Автор")
        self.quotes_tree.heading("Тема", text="Тема")
        
        self.quotes_tree.column("ID", width=50)
        self.quotes_tree.column("Цитата", width=500)
        self.quotes_tree.column("Автор", width=150)
        self.quotes_tree.column("Тема", width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(quotes_display_frame, orient=tk.VERTICAL, command=self.quotes_tree.yview)
        self.quotes_tree.configure(yscrollcommand=scrollbar.set)
        
        self.quotes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_add_tab(self):
        """Setup the add quote tab"""
        # Main frame
        main_frame = ttk.Frame(self.add_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Quote text
        ttk.Label(main_frame, text="Текст цитаты:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.quote_text_entry = scrolledtext.ScrolledText(main_frame, height=6, width=60, wrap=tk.WORD)
        self.quote_text_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Author
        ttk.Label(main_frame, text="Автор:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.author_entry = ttk.Entry(main_frame, width=50)
        self.author_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Topic
        ttk.Label(main_frame, text="Тема:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.topic_entry = ttk.Entry(main_frame, width=50)
        self.topic_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        save_btn = ttk.Button(buttons_frame, text="💾 Сохранить цитату", command=self.save_new_quote)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(buttons_frame, text="🗑️ Очистить поля", command=self.clear_add_form)
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def setup_history_tab(self):
        """Setup the history tab"""
        # Main frame
        main_frame = ttk.Frame(self.history_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Filters frame
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация истории", padding="10")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Author filter
        ttk.Label(filter_frame, text="Автор:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.history_author_var = tk.StringVar(value="Все")
        self.history_author_combo = ttk.Combobox(filter_frame, textvariable=self.history_author_var, width=30)
        self.history_author_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Topic filter
        ttk.Label(filter_frame, text="Тема:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.history_topic_var = tk.StringVar(value="Все")
        self.history_topic_combo = ttk.Combobox(filter_frame, textvariable=self.history_topic_var, width=30)
        self.history_topic_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Apply filter button
        apply_filter_btn = ttk.Button(filter_frame, text="🔍 Применить фильтр", 
                                     command=self.display_filtered_history)
        apply_filter_btn.grid(row=0, column=2, rowspan=2, padx=20, pady=5)
        
        # History display
        history_display_frame = ttk.LabelFrame(main_frame, text="История цитат", padding="10")
        history_display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for history
        columns = ("Дата", "Цитата", "Автор", "Тема")
        self.history_tree = ttk.Treeview(history_display_frame, columns=columns, show="headings", height=15)
        
        self.history_tree.heading("Дата", text="Дата и время")
        self.history_tree.heading("Цитата", text="Цитата")
        self.history_tree.heading("Автор", text="Автор")
        self.history_tree.heading("Тема", text="Тема")
        
        self.history_tree.column("Дата", width=150)
        self.history_tree.column("Цитата", width=450)
        self.history_tree.column("Автор", width=150)
        self.history_tree.column("Тема", width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(history_display_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        clear_history_btn = ttk.Button(buttons_frame, text="🗑️ Очистить всю историю", 
                                      command=self.clear_all_history)
        clear_history_btn.pack(side=tk.RIGHT, padx=5)
        
        refresh_btn = ttk.Button(buttons_frame, text="🔄 Обновить историю", 
                                command=self.display_filtered_history)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
    
    def refresh_filters(self):
        """Refresh all filter dropdowns"""
        authors = ["Все"] + self.quote_manager.get_all_authors()
        topics = ["Все"] + self.quote_manager.get_all_topics()
        
        # Update generator tab filters
        self.gen_author_combo['values'] = authors
        self.gen_topic_combo['values'] = topics
        
        # Update quotes tab filters
        self.quotes_author_combo['values'] = authors
        self.quotes_topic_combo['values'] = topics
        
        # Update history tab filters
        self.history_author_combo['values'] = authors
        self.history_topic_combo['values'] = topics
        
        # Update displays
        self.display_filtered_quotes()
        self.display_filtered_history()
        
        self.status_var.set("Фильтры обновлены")
    
    def generate_quote(self):
        """Generate and display a random quote"""
        author = self.gen_author_var.get() if self.gen_author_var.get() != "Все" else None
        topic = self.gen_topic_var.get() if self.gen_topic_var.get() != "Все" else None
        
        quote = self.quote_manager.get_filtered_random_quote(author, topic)
        
        if quote:
            # Display quote
            self.quote_text.config(state='normal')
            self.quote_text.delete(1.0, tk.END)
            display_text = f'"{quote["text"]}"\n\n— {quote["author"]}\n📌 Тема: {quote["topic"]}'
            self.quote_text.insert(1.0, display_text)
            self.quote_text.config(state='disabled')
            
            # Add to history
            self.quote_manager.add_to_history(quote)
            self.display_filtered_history()
            self.status_var.set(f"✅ Цитата сгенерирована! Всего в истории: {len(self.quote_manager.history)}")
        else:
            messagebox.showwarning("Нет цитат", 
                                 "Нет цитат, соответствующих выбранным фильтрам!\nПопробуйте другие фильтры или добавьте новые цитаты.")
            self.status_var.set("❌ Нет цитат по выбранным фильтрам")
    
    def display_filtered_quotes(self):
        """Display filtered quotes in the quotes tab"""
        # Clear existing items
        for item in self.quotes_tree.get_children():
            self.quotes_tree.delete(item)
        
        author = self.quotes_author_var.get() if self.quotes_author_var.get() != "Все" else None
        topic = self.quotes_topic_var.get() if self.quotes_topic_var.get() != "Все" else None
        
        quotes = self.quote_manager.get_quotes_by_filter(author, topic)
        
        for idx, quote in enumerate(quotes, 1):
            display_text = quote["text"][:100] + "..." if len(quote["text"]) > 100 else quote["text"]
            self.quotes_tree.insert("", tk.END, values=(
                idx,
                display_text,
                quote["author"],
                quote["topic"]
            ))
        
        self.status_var.set(f"📖 Показано цитат: {len(quotes)}")
    
    def display_filtered_history(self):
        """Display filtered history in the history tab"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        author = self.history_author_var.get() if self.history_author_var.get() != "Все" else None
        topic = self.history_topic_var.get() if self.history_topic_var.get() != "Все" else None
        
        history = self.quote_manager.get_history_by_filter(author, topic)
        
        for entry in reversed(history):  # Show newest first
            display_text = entry["text"][:100] + "..." if len(entry["text"]) > 100 else entry["text"]
            self.history_tree.insert("", tk.END, values=(
                entry["timestamp"],
                display_text,
                entry["author"],
                entry["topic"]
            ))
        
        self.status_var.set(f"📜 Показано записей в истории: {len(history)}")
    
    def save_new_quote(self):
        """Save a new quote with validation"""
        text = self.quote_text_entry.get(1.0, tk.END).strip()
        author = self.author_entry.get().strip()
        topic = self.topic_entry.get().strip()
        
        success, message = self.quote_manager.add_quote(text, author, topic)
        
        if success:
            messagebox.showinfo("Успех", message)
            self.clear_add_form()
            self.refresh_filters()
            self.status_var.set("✅ Новая цитата добавлена!")
        else:
            messagebox.showerror("Ошибка валидации", message)
            self.status_var.set(f"❌ Ошибка: {message}")
    
    def clear_add_form(self):
        """Clear the add quote form"""
        self.quote_text_entry.delete(1.0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.topic_entry.delete(0, tk.END)
        self.status_var.set("Форма очищена")
    
    def clear_all_history(self):
        """Clear all history with confirmation"""
        if messagebox.askyesno("Очистка истории", 
                               "Вы уверены, что хотите очистить всю историю?\nЭто действие нельзя отменить."):
            self.quote_manager.clear_history()
            self.display_filtered_history()
            self.status_var.set("🗑️ История полностью очищена")
            messagebox.showinfo("Успех", "История успешно очищена!")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()
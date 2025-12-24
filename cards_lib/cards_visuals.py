import tkinter as tk
from tkinter import messagebox
from typing import Dict, Any, Callable

class CardsVis:
    def __init__(self, root: tk.Tk, cards_manager, title: str = "Flashcard App"):
        self.root = root
        self.cards_manager = cards_manager
        self.root.title(title)
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        self.is_front = True
        self.current_card = {}
        self.callbacks = {}
        
        self.create_widgets()
        self.update_card_display()
    
    def register_callback(self, event: str, callback: Callable):
        self.callbacks[event] = callback
    
    def create_widgets(self):
        title_label = tk.Label(self.root, text="Foreign Language Flashcards", 
                              font=("Arial", 20, "bold"), bg='#f0f0f0', fg='#333')
        title_label.pack(pady=10)
        
        self.card_frame = tk.Frame(self.root, bg='white', relief='raised', bd=3)
        self.card_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        self.card_label = tk.Label(self.card_frame, text="", wraplength=500, 
                                  font=("Arial", 18, "bold"), bg='white', fg='#333',
                                  justify='center', height=6)
        self.card_label.pack(pady=30)
        
        # Control buttons
        btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        btn_frame.pack(pady=20)
        
        self.flip_btn = tk.Button(btn_frame, text="Flip Card", command=self.flip_card,
                                 font=("Arial", 12, "bold"), bg='#4CAF50', fg='white',
                                 relief='flat', padx=20, pady=8)
        self.flip_btn.pack(side=tk.LEFT, padx=10)
        
        self.next_btn = tk.Button(btn_frame, text="Next Card", command=self.next_card,
                                 font=("Arial", 12, "bold"), bg='#2196F3', fg='white',
                                 relief='flat', padx=20, pady=8)
        self.next_btn.pack(side=tk.LEFT, padx=10)
        
        diff_frame = tk.Frame(self.root, bg='#f0f0f0')
        diff_frame.pack(pady=10)
        
        self.easy_btn = tk.Button(diff_frame, text="Easy", command=self.on_easy,
                                 font=("Arial", 11), bg='#8BC34A', fg='white', state=tk.DISABLED,
                                 relief='flat', padx=15)
        self.easy_btn.pack(side=tk.LEFT, padx=5)
        
        self.medium_btn = tk.Button(diff_frame, text="Medium", command=self.on_medium,
                                   font=("Arial", 11), bg='#FF9800', fg='white', state=tk.DISABLED,
                                   relief='flat', padx=15)
        self.medium_btn.pack(side=tk.LEFT, padx=5)
        
        self.hard_btn = tk.Button(diff_frame, text="Hard", command=self.on_hard,
                                 font=("Arial", 11), bg='#F44336', fg='white', state=tk.DISABLED,
                                 relief='flat', padx=15)
        self.hard_btn.pack(side=tk.LEFT, padx=5)
        
        mgmt_frame = tk.Frame(self.root, bg='#f0f0f0')
        mgmt_frame.pack(pady=10)
        
        tk.Button(mgmt_frame, text="Add Card", command=self.add_card_dialog,
                 font=("Arial", 10), bg='#9C27B0', fg='white', relief='flat', padx=15).pack(side=tk.LEFT, padx=5)
        tk.Button(mgmt_frame, text="Stats", command=self.show_stats,
                 font=("Arial", 10), bg='#607D8B', fg='white', relief='flat', padx=15).pack(side=tk.LEFT, padx=5)
    
    def update_card_display(self):
        """Show current card."""
        self.current_card = self.cards_manager.get_next_card()
        if not self.current_card:
            messagebox.showinfo("Complete!", "No cards available!")
            return
        
        self.card_label.config(text=self.current_card["front"])
        self.is_front = True
        self.flip_btn.config(state=tk.NORMAL, text="Flip Card")
        self.set_difficulty_buttons_state(tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL)
    
    def flip_card(self):
        if self.is_front:
            self.card_label.config(text=self.current_card["back"])
            self.is_front = False
            self.flip_btn.config(text="Flip Back")
            self.set_difficulty_buttons_state(tk.NORMAL)
        else:
            self.card_label.config(text=self.current_card["front"])
            self.is_front = True
            self.flip_btn.config(text="Flip Card")
            self.set_difficulty_buttons_state(tk.DISABLED)
    
    def set_difficulty_buttons_state(self, state):
        self.easy_btn.config(state=state)
        self.medium_btn.config(state=state)
        self.hard_btn.config(state=state)
    
    def next_card(self):
        self.update_card_display()
    
    def on_easy(self):
        self.rate_card("easy")
    
    def on_medium(self):
        self.rate_card("medium")
    
    def on_hard(self):
        self.rate_card("hard")
    
    def rate_card(self, difficulty: str):
        if "rate_card" in self.callbacks:
            self.callbacks["rate_card"](self.current_card, difficulty)
        self.update_card_display()
    
    def add_card_dialog(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("Add New Card")
        add_win.geometry("400x300")
        add_win.transient(self.root)
        add_win.grab_set()
        
        tk.Label(add_win, text="Foreign Word:", font=("Arial", 12)).pack(pady=10)
        front_entry = tk.Entry(add_win, font=("Arial", 12), width=30)
        front_entry.pack(pady=5)
        
        tk.Label(add_win, text="Translation:", font=("Arial", 12)).pack(pady=10)
        back_entry = tk.Entry(add_win, font=("Arial", 12), width=30)
        back_entry.pack(pady=5)
        
        def save_card():
            front = front_entry.get().strip()
            back = back_entry.get().strip()
            if front and back:
                if "add_card" in self.callbacks:
                    self.callbacks["add_card"](front, back)
                messagebox.showinfo("Success", "Card added!")
                add_win.destroy()
            else:
                messagebox.showerror("Error", "Please fill both fields!")
        
        tk.Button(add_win, text="Add Card", command=save_card, 
                 bg='#4CAF50', fg='white', font=("Arial", 12), pady=10).pack(pady=20)
    
    def show_stats(self):
        """Display statistics."""
        stats = self.cards_manager.get_stats()
        if stats["total"] == 0:
            messagebox.showinfo("Stats", "No cards reviewed yet!")
            return
        
        stats_text = f"""
Total Reviewed: {stats["total"]}
Easy: {stats["easy"]} ({stats["easy_pct"]:.1f}%)
Medium: {stats["medium"]} ({stats["medium_pct"]:.1f}%)
Hard: {stats["hard"]} ({stats["hard_pct"]:.1f}%)
Deck Size: {stats["deck_size"]}
        """
        messagebox.showinfo("Learning Stats", stats_text)


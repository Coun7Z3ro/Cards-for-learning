from .data_manager import CardsManager
from .cards_visuals import CardsVis
import tkinter as tk

class FlashcardApp:
    def __init__(self, deck_file: str = 'flashcards.json', title: str = "Flashcard App"):
        self.manager = CardsManager(deck_file)
        self.setup_callbacks()
        
        self.root = tk.Tk()
        self.vis = CardsVis(self.root, self.manager, title)
        self.vis.register_callback("add_card", self.manager.add_card)
        self.vis.register_callback("rate_card", self.manager.rate_card_by_content)

    def setup_callbacks(self):
        pass

    def run(self):
        self.root.mainloop()

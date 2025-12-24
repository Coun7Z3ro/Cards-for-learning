import json
import os
import random
from typing import List, Dict, Any

class CardsManager:
    def __init__(self, deck_file: str = 'flashcards.json'):
        self.deck_file = deck_file
        self.flashcards: List[Dict[str, Any]] = self.load_deck()
        self.card_history: List[str] = []

    def load_deck(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.deck_file):
            try:
                with open(self.deck_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_deck(self):
        with open(self.deck_file, 'w', encoding='utf-8') as f:
            json.dump(self.flashcards, f, ensure_ascii=False, indent=2)

    def add_card(self, front: str, back: str, difficulty: str = "medium"):
        card = {"front": front, "back": back, "difficulty": difficulty}
        self.flashcards.append(card)
        self.save_deck()

    def rate_card(self, index: int, difficulty: str):
        if 0 <= index < len(self.flashcards):
            card = self.flashcards.pop(index)
            card["difficulty"] = difficulty
            self.card_history.append(difficulty)
            if difficulty == "easy":
                self.flashcards.append(card)
            elif difficulty == "medium":
                self.flashcards.insert(len(self.flashcards)//2, card)
            else:  # hard
                self.flashcards.insert(0, card)
            self.save_deck()

    def rate_card_by_content(self, card: Dict[str, Any], difficulty: str):
        """Rate card by content dict (for GUI callbacks)."""
        if card in self.flashcards:
            index = self.flashcards.index(card)
            self.rate_card(index, difficulty)

    def get_next_card(self) -> Dict[str, Any]:
        if not self.flashcards:
            return {}
        random.shuffle(self.flashcards)
        return self.flashcards[0]

    def get_stats(self) -> Dict[str, Any]:
        total = len(self.card_history)
        if total == 0:
            return {"total": 0, "easy": 0, "medium": 0, "hard": 0, "deck_size": len(self.flashcards)}
        easy = self.card_history.count("easy")
        medium = self.card_history.count("medium")
        hard = self.card_history.count("hard")
        return {
            "total": total, "easy": easy, "medium": medium, "hard": hard,
            "deck_size": len(self.flashcards),
            "easy_pct": easy/total*100, "medium_pct": medium/total*100, "hard_pct": hard/total*100
        }

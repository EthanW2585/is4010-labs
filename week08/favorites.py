"""JSON-backed, case-insensitive favorite locations."""

import json
from pathlib import Path


class FavoritesManager:
    def __init__(self, filename):
        self.filename = Path(filename)
        self.favorites = self._load()

    def _load(self):
        try:
            with self.filename.open('r', encoding='utf-8') as file:
                data = json.load(file)
            if isinstance(data, dict):
                return {str(name): location for name, location in data.items()
                        if isinstance(name, str) and isinstance(location, str)}
        except (OSError, ValueError, TypeError):
            pass
        return {}

    def _save(self):
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        with self.filename.open('w', encoding='utf-8') as file:
            json.dump(self.favorites, file, indent=4)

    def _matching_name(self, name):
        return next((saved for saved in self.favorites
                     if saved.casefold() == name.casefold()), None)

    def add(self, name, location):
        if self._matching_name(name) is not None:
            return False
        self.favorites[name] = location
        self._save()
        return True

    def remove(self, name):
        saved = self._matching_name(name)
        if saved is None:
            return False
        del self.favorites[saved]
        self._save()
        return True

    def list_all(self):
        return self.favorites.copy()

    def get_location(self, name):
        saved = self._matching_name(name)
        return self.favorites[saved] if saved is not None else None

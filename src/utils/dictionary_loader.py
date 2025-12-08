from typing import Set, Optional
import json
from pathlib import Path


class DictionaryLoader:
    """
    Dictionary Loader.
    """

    def __init__(self, dictionary_dir: Optional[str] = None):
        """
        Initialize dictionary loader.

        Args:
            dictionary_dir (str, optional): Directory with dictionary files.
                                           If None, uses default location.
        """
        if dictionary_dir is None:
            current_dir = Path(__file__).parent
            self.dictionary_dir = current_dir.parent.parent / "data" / "dictionaries"
        else:
            self.dictionary_dir = Path(dictionary_dir)

        self.dictionary_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def load_formal_dictionary() -> Set[str]:
        """Loads the dictionary of formal vocabulary."""
        formal_words = {
            "следовательно",
            "соответственно",
            "вследствие",
            "осуществлять",
            "являться",
            "настоящий",
            "данный",
            "присутствовать",
            "отсутствовать",
            "вышеуказанный",
            "нижеследующий",
            "надлежащий",
            "установленный",
            "обусловливать",
            "характеризоваться",
            "представляться",
            "таким образом",
            "в соответствии с",
            "на основании",
            "в результате",
            "в течение",
            "посредством",
            "относительно",
            "применительно",
            "аналогично",
            "констатировать",
            "свидетельствовать",
            "преобладать",
            "доминировать",
            "реализовывать",
            "формализовать",
            "интерпретировать",
            "анализировать",
            "исследовать",
            "эксперимент",
            "методология",
            "парадигма",
            "концепция",
            "теоретический",
            "практический",
            "эмпирический",
            "фундаментальный",
        }
        return formal_words

    @staticmethod
    def load_informal_dictionary() -> Set[str]:
        """Loads a dictionary of informal vocabulary."""
        informal_words = {
            "короче",
            "типа",
            "как бы",
            "вот",
            "это",
            "ну",
            "так сказать",
            "знаешь",
            "понимаешь",
            "слушай",
            "кстати",
            "вообще",
            "прикинь",
            "обалдеть",
            "клево",
            "отстой",
            "нормально",
            "понятно",
            "ладно",
            "окей",
            "чувак",
            "братан",
            "девчонка",
            "мужик",
            "тачка",
            "хата",
            "бабки",
            "тусовка",
        }
        return informal_words

    @staticmethod
    def load_scientific_dictionary() -> Set[str]:
        """Loads dictionary of scientific terms."""
        return {
            "гипотеза",
            "теория",
            "эксперимент",
            "методология",
            "анализ",
            "синтез",
            "дедукция",
            "индукция",
            "параметр",
            "переменная",
            "константа",
            "коэффициент",
            "корреляция",
            "регрессия",
            "дисперсия",
            "отклонение",
            "алгоритм",
            "модель",
            "система",
            "структура",
            "процесс",
            "результат",
            "заключение",
            "вывод",
            "объект",
            "субъект",
            "феномен",
            "явление",
        }

    def load_emotional_dictionary(self) -> Set[str]:
        """Loads dictionary of emotional words."""
        return {
            "прекрасный",
            "ужасный",
            "восхитительный",
            "отвратительный",
            "счастливый",
            "грустный",
            "радостный",
            "печальный",
            "любимый",
            "ненавистный",
            "милый",
            "противный",
            "великолепный",
            "отвратительный",
            "потрясающий",
            "ужасный",
            "невероятный",
            "невыносимый",
            "чудесный",
            "кошмарный",
            "очаровательный",
            "отвратительный",
            "прелестный",
            "ужасный",
            "блестящий",
            "ужасный",
            "изумительный",
            "отвратительный",
        }

    def save_custom_dictionary(self, name: str, words: Set[str]) -> bool:
        """Saves custom dictionary to file."""
        try:
            file_path = self.dictionary_dir / f"{name}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dumps(list(words), f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def load_custom_dictionary(self, name: str) -> Optional[Set[str]]:
        """Loads custom dictionary from file."""
        try:
            file_path = self.dictionary_dir / f"{name}.json"
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    words = json.load(f)
                return set(words)
        except Exception:
            pass
        return None

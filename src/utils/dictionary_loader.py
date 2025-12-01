from typing import Set


class DictionaryLoader:
    """
    Dictionary Loader.
    """

    def __init__(self):
        pass

    @staticmethod
    def load_formal_dictionary() -> Set[str]:
        """Loads the dictionary of formal vocabulary."""
        formal_words = {
            'следовательно', 'соответственно', 'вследствие', 'осуществлять',
            'являться', 'настоящий', 'данный', 'присутствовать', 'отсутствовать',
            'вышеуказанный', 'нижеследующий', 'надлежащий', 'установленный',
            'обусловливать', 'характеризоваться', 'представляться'
        }
        return formal_words

    @staticmethod
    def load_informal_dictionary() -> Set[str]:
        """Loads a dictionary of informal vocabulary."""
        informal_words = {
            'короче', 'типа', 'как бы', 'вот', 'это', 'ну', 'так сказать',
            'знаешь', 'понимаешь', 'слушай', 'кстати', 'вообще'
        }
        return informal_words
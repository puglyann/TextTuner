import os
from typing import Optional


class FileHandler:
    """
    A class for working with files.
    """

    @staticmethod
    def read_text_file(file_path: str, encoding: str = 'utf-8') -> str:
        """Reads a text file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        if not file_path.lower().endswith('.txt'):
            raise ValueError("Поддерживаются только файлы с расширением .txt")

        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            for enc in ['cp1251', 'koi8-r', 'iso-8859-5']:
                try:
                    with open(file_path, 'r', encoding=enc) as file:
                        return file.read()
                except UnicodeDecodeError:
                    continue
            raise ValueError(f"Не удалось декодировать файл {file_path}")

    @staticmethod
    def validate_file_size(file_path: str, max_size_mb: int = 10) -> bool:
        """Checks the file size."""
        size_in_mb = os.path.getsize(file_path) / (1024 * 1024)
        return size_in_mb <= max_size_mb

    @staticmethod
    def detect_encoding(file_path: str) -> Optional[str]:
        """Defines the encoding of the file."""
        encodings = ['utf-8', 'cp1251', 'koi8-r', 'iso-8859-5']

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    file.read()
                return encoding
            except UnicodeDecodeError:
                continue

        return None
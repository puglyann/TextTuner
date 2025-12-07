import os
from typing import Optional, List
from pathlib import Path
import chardet


class FileHandler:
    """
    A class for working with files.
    """

    def __init__(self):
        self.supported_extensions = {'.txt', '.md', '.json'}

    @staticmethod
    def read_text_file(file_path: str, encoding: str = 'utf-8') -> str:
        """Reads a text file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        file_ext = Path(file_path).suffix.lower()
        if file_ext not in {'.txt', '.md', '.json', '.csv'}:
            print(f"Предупреждение: Файл имеет неподдерживаемое расширение: {file_ext}")

        with open(file_path, 'rb') as f:
            raw_data = f.read()
            detected = chardet.detect(raw_data)
            detected_encoding = detected['encoding'] or encoding

        try:
            return raw_data.decode(detected_encoding)
        except UnicodeDecodeError:
            for enc in ['utf-8', 'cp1251', 'koi8-r', 'iso-8859-5']:
                try:
                    return raw_data.decode(enc)
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

    def find_text_files(self, directory_path: str, recursive: bool = True) -> List[str]:
        """Finds all text files in directory."""
        path = Path(directory_path)

        if not path.exists():
            raise FileNotFoundError(f"Директория не найдена: {directory_path}")

        if not path.is_dir():
            raise ValueError(f"Путь не является директорией: {directory_path}")

        files = []

        if recursive:
            for ext in self.supported_extensions:
                files.extend(str(p) for p in path.rglob(f"*{ext}"))
        else:
            for ext in self.supported_extensions:
                files.extend(str(p) for p in path.glob(f"*{ext}"))

        return sorted(files)

    @staticmethod
    def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> None:
        """Writes content to file."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)

    def get_file_info(self, file_path: str) -> dict:
        """Returns information about file."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        return {
            'name': path.name,
            'size_bytes': path.stat().st_size,
            'size_mb': path.stat().st_size / (1024 * 1024),
            'modified': path.stat().st_mtime,
            'extension': path.suffix.lower(),
            'encoding': self.detect_encoding(file_path)
        }
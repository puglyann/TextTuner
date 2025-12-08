import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Запуск TextTuner...")
print(f"Текущая директория: {os.getcwd()}")
print(f"Директория скрипта: {os.path.dirname(os.path.abspath(__file__))}")

required_files = [
    "src/main.py",
    "src/config/style_configs.py",
    "src/core/text_analyzer.py",
    "src/models/text_models.py",
    "src/utils/file_handler.py",
]

print("\nПроверка файлов:")
for file in required_files:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} - ОТСУТСТВУЕТ!")

print("\n" + "=" * 60)

try:
    from src.main import main

    print("Импорт успешен! Запуск TextTuner...")
    print("=" * 60 + "\n")

    main()

except ImportError as e:
    print(f"ОШИБКА ИМПОРТА: {e}")
    print("\nВозможные причины:")
    print("1. Файлы находятся не в правильных местах")
    print("2. Отсутствуют __init__.py файлы")
    print("3. Неправильные импорты в коде")

    print("\nТекущая структура проекта:")
    for root, dirs, files in os.walk("."):
        # Пропускаем скрытые директории
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        level = root.count(os.sep) - 1
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 2 * (level + 1)
        for f in files:
            if f.endswith(".py"):
                print(f"{subindent}{f}")

    sys.exit(1)
except Exception as e:
    print(f"ОШИБКА ВЫПОЛНЕНИЯ: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

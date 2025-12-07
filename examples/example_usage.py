import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.main import TextTuner


def main():
    """Main usage example."""
    tuner = TextTuner()

    text = """
        Я думаю, что этот проект очень хороший и интересный.
        Он помогает людям улучшать свои тексты.
        Мне нравится работать с этой программой.
    """

    print("Пример 1: Анализ текста для научного стиля")
    print("=" * 60)

    result = tuner.analyze_text(text, "научный")
    print(result.generate_report("text"))

    print("\n" + "=" * 60)
    print("Пример 2: Адаптация текста к официально-деловому стилю")
    print("=" * 60)

    adaptation = tuner.adapt_text(text, "официально-деловой")
    print(f"Оригинальный текст:\n{adaptation['original_text']}")
    print(f"\nАдаптированный текст:\n{adaptation['adapted_text']}")
    print(f"\nРекомендации:")
    for i, rec in enumerate(adaptation['analysis'].recommendations, 1):
        print(f"  {i}. {rec}")

    print("\n" + "=" * 60)
    print("Пример 3: Анализ из файла")
    print("=" * 60)

    example_file = os.path.join(os.path.dirname(__file__), "example_scientific.txt")
    if os.path.exists(example_file):
        try:
            file_result = tuner.analyze_file(example_file, "научный")
            print(f"Соответствие научному стилю: {file_result.similarity_score:.1%}")
        except Exception as e:
            print(f"Ошибка анализа файла: {e}")
    else:
        print(f"Файл примера не найден: {example_file}")
        print("Создайте файлы примеров в папке examples/")


if __name__ == "__main__":
    main()
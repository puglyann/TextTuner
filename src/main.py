"""
TextTuner is a tool for adapting text to a target style.

The main module of the application provides an interface for analyzing and adapting text.
"""

import sys
import os
import argparse
from typing import Dict, Any, Optional

from .core.text_analyzer import TextAnalyzer
from .core.style_adapter import StyleAdapter
from .core.statistics_calculator import StatisticsCalculator
from .models.text_models import TextDocument, AnalysisResult
from .models.style_models import StyleProfile
from .utils.file_handler import FileHandler
from .config.style_configs import get_style_config, get_available_styles


class TextTuner:
    """
    The main class of the TextTuner application.

    Coordinates the operation of all system components: file reading, text analysis,
    style adaptation, and report generation.

    Attributes:
    text_analyzer (TextAnalyzer): Text analyzer.
    style_adapter (StyleAdapter): Style adapter.
    statistics_calculator (StatisticsCalculator): Statistics calculator.
    file_handler (FileHandler): File handler.
    """

    def __init__(self):
        """Initialize TextTuner with all necessary components."""
        self.text_analyzer = TextAnalyzer()
        self.style_adapter = StyleAdapter()
        self.statistics_calculator = StatisticsCalculator()
        self.file_handler = FileHandler()

    def analyze_text(self, text: str, target_style: str) -> AnalysisResult:
        """
        Analyze text and compare it to target style.

        Args:
            text (str): Input text to analyze
            target_style (str): Target style name

        Returns:
            AnalysisResult: Analysis results with recommendations
        """
        style_config = get_style_config(target_style)
        if not style_config:
            available_styles = list(get_available_styles().keys())
            raise ValueError(f"Style '{target_style}' not found. Available styles: {available_styles}")

        text_doc = TextDocument(raw_text=text)

        style_metrics = self.text_analyzer.analyze_text(text)

        style_profile = StyleProfile(
            name=target_style,
            description=style_config['description'],
            target_metrics=style_config['target_metrics']
        )

        similarity_score = style_profile.calculate_similarity(style_metrics)

        recommendations = self.style_adapter.generate_recommendations(
            style_metrics,
            style_profile
        )

        result = AnalysisResult(
            text_document=text_doc,
            style_metrics=style_metrics,
            target_style=target_style,
            similarity_score=similarity_score,
            recommendations=recommendations
        )

        return result

    def analyze_file(self, file_path: str, target_style: str) -> AnalysisResult:
        """
        Analyze text from file.

        Args:
            file_path (str): Path to text file
            target_style (str): Target style name

        Returns:
            AnalysisResult: Analysis results
        """
        try:
            text = self.file_handler.read_text_file(file_path)
        except Exception as file_err:
            raise ValueError(f"Ошибка чтения файла {file_path}: {file_err}")

        return self.analyze_text(text, target_style)

    def adapt_text(self, text: str, target_style: str) -> Dict[str, Any]:
        """
        Adapt text to target style with specific transformations.

        Args:
            text (str): Input text
            target_style (str): Target style name

        Returns:
            Dict with original text, adapted text, and changes made
        """
        analysis_result = self.analyze_text(text, target_style)

        adapted_text = self.style_adapter.adapt_text(
            text,
            analysis_result.style_metrics,
            get_style_config(target_style)
        )

        return {
            'original_text': text,
            'adapted_text': adapted_text,
            'analysis': analysis_result,
            'style': target_style
        }

    def batch_analyze(self, directory_path: str, target_style: str) -> Dict[str, AnalysisResult]:
        """
        Analyze multiple files in directory.

        Args:
            directory_path (str): Path to directory with text files
            target_style (str): Target style name

        Returns:
            Dict mapping filename to AnalysisResult
        """
        results = {}

        try:
            text_files = self.file_handler.find_text_files(directory_path)
        except Exception as find_err:
            print(f"Ошибка поиска файлов: {find_err}")
            return results

        for file_path in text_files:
            try:
                result = self.analyze_file(file_path, target_style)
                results[os.path.basename(file_path)] = result
            except Exception as analysis_err:
                print(f"Ошибка анализа {file_path}: {analysis_err}")

        return results


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description='TextTuner: Адаптация текста под целевой стиль',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s --text "Ваш текст здесь" --style научный
  %(prog)s --file input.txt --style художественный --output report.json
  %(prog)s --list-styles
        """
    )

    parser.add_argument(
        '--text',
        type=str,
        help='Текст для анализа (если не указан --file)'
    )

    parser.add_argument(
        '--file',
        type=str,
        help='Путь к файлу с текстом'
    )

    parser.add_argument(
        '--style',
        type=str,
        required=True,
        choices=['научный', 'художественный', 'официально-деловой', 'разговорный'],
        help='Целевой стиль для анализа'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='Путь для сохранения отчета (JSON формат)'
    )

    parser.add_argument(
        '--format',
        type=str,
        choices=['text', 'json'],
        default='text',
        help='Формат вывода отчета (по умолчанию: text)'
    )

    parser.add_argument(
        '--list-styles',
        action='store_true',
        help='Показать доступные стили и выйти'
    )

    parser.add_argument(
        '--adapt',
        action='store_true',
        help='Выполнить адаптацию текста (показать изменения)'
    )

    return parser


def main() -> None:
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args()

    if args.list_styles:
        print("Доступные стили:")
        for style, desc in get_available_styles().items():
            print(f"  • {style}: {desc}")
        return

    tuner = TextTuner()

    try:
        if args.file and args.text:
            parser.error("Укажите либо --text, либо --file, но не оба")
        elif args.file:
            if not os.path.exists(args.file):
                parser.error(f"Файл не найден: {args.file}")

            result = tuner.analyze_file(args.file, args.style)

        elif args.text:
            result = tuner.analyze_text(args.text, args.style)

        else:
            parser.error("Необходимо указать --text или --file")

        if args.adapt:
            text_to_adapt = args.text if args.text else tuner.file_handler.read_text_file(args.file)
            adaptation = tuner.adapt_text(text_to_adapt, args.style)

            print("\n" + "="*60)
            print("РЕЗУЛЬТАТ АДАПТАЦИИ ТЕКСТА")
            print("="*60)
            print(f"\nОригинальный текст:\n{adaptation['original_text'][:500]}...")
            print(f"\n\nАдаптированный текст:\n{adaptation['adapted_text'][:500]}...")
            print(f"\n\nЦелевой стиль: {args.style}")

            print("\n" + result.generate_report('text'))

        else:
            output = result.generate_report(args.format)

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"Отчет сохранен в: {args.output}")
            else:
                print(output)

    except Exception as main_err:
        print(f"Ошибка: {main_err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


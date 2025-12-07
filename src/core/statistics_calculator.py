import statistics
from typing import Dict, List, Tuple, Any, Optional
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'DejaVu Sans'
rcParams['axes.unicode_minus'] = False


class StatisticsCalculator:
    """
    Calculator for statistical analysis of text metrics.
    """

    def __init__(self):
        """Initialize statistics calculator."""
        pass

    @staticmethod
    def calculate_descriptive_stats(metrics_list: List[Dict[str, float]]) -> Dict[str, Dict[str, float]]:
        """
        Calculate descriptive statistics for a list of metrics.

        Args:
            metrics_list (List[Dict]): List of metric dictionaries

        Returns:
            Dict[str, Dict[str, float]]: Statistics for each metric
        """
        if not metrics_list:
            return {}

        metric_names = set()
        for metrics in metrics_list:
            metric_names.update(metrics.keys())

        stats = {}
        for metric_name in metric_names:
            values = []
            for metrics in metrics_list:
                if metric_name in metrics:
                    values.append(metrics[metric_name])

            if values:
                stats[metric_name] = {
                    'mean': statistics.mean(values),
                    'median': statistics.median(values),
                    'std': statistics.stdev(values) if len(values) > 1 else 0.0,
                    'min': min(values),
                    'max': max(values),
                    'count': len(values)
                }

        return stats

    @staticmethod
    def calculate_style_deviation(current_metrics: Dict[str, float],
                                  target_metrics: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        """
        Calculate deviation from target style metrics.

        Args:
            current_metrics (Dict): Current text metrics
            target_metrics (Dict): Target style metrics configuration

        Returns:
            Dict: Deviation analysis for each metric
        """
        deviation_analysis = {}

        for metric_name, target_config in target_metrics.items():
            if metric_name in current_metrics:
                current_value = current_metrics[metric_name]
                target_value = target_config.get('target', 0)
                tolerance = target_config.get('tolerance', 0.1)

                absolute_diff = abs(current_value - target_value)
                relative_diff = absolute_diff / target_value if target_value != 0 else 0.0

                within_tolerance = absolute_diff <= tolerance

                deviation_analysis[metric_name] = {
                    'current': current_value,
                    'target': target_value,
                    'absolute_diff': absolute_diff,
                    'relative_diff': relative_diff,
                    'within_tolerance': within_tolerance,
                    'tolerance': tolerance,
                    'weight': target_config.get('weight', 1.0)
                }

        return deviation_analysis

    def calculate_overall_score(self,
                                deviation_analysis: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate overall style matching score.

        Args:
            deviation_analysis (Dict): Deviation analysis for each metric

        Returns:
            float: Overall score (0-1)
        """
        if not deviation_analysis:
            return 0.0

        weighted_scores = []
        total_weight = 0.0

        for metric_name, analysis in deviation_analysis.items():
            weight = analysis.get('weight', 1.0)
            relative_diff = analysis.get('relative_diff', 1.0)

            metric_score = max(0.0, 1.0 - min(relative_diff, 1.0))
            weighted_scores.append(metric_score * weight)
            total_weight += weight

        if total_weight == 0:
            return 0.0

        return sum(weighted_scores) / total_weight

    def generate_radar_chart(self,
                             current_metrics: Dict[str, float],
                             target_metrics: Dict[str, Any],
                             save_path: Optional[str] = None) -> plt.Figure:
        """
        Generate radar chart comparing current vs target metrics.

        Args:
            current_metrics (Dict): Current metrics
            target_metrics (Dict): Target metrics configuration
            save_path (str, optional): Path to save the chart

        Returns:
            plt.Figure: Generated figure
        """
        metrics = []
        current_values = []
        target_values = []

        for metric_name, target_config in target_metrics.items():
            if metric_name in current_metrics:
                metrics.append(self._format_metric_name(metric_name))
                current_values.append(current_metrics[metric_name])
                target_values.append(target_config.get('target', 0))

        if not metrics:
            raise ValueError("No matching metrics found for radar chart")

        max_val = max(max(current_values), max(target_values))
        if max_val > 0:
            current_normalized = [v / max_val for v in current_values]
            target_normalized = [v / max_val for v in target_values]
        else:
            current_normalized = current_values
            target_normalized = target_values

        angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
        angles += angles[:1]  # Close the polygon

        current_normalized += current_normalized[:1]
        target_normalized += target_normalized[:1]
        metrics += metrics[:1]

        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))

        ax.plot(angles, current_normalized, 'o-', linewidth=2, label='Текущий текст', color='blue')
        ax.fill(angles, current_normalized, alpha=0.25, color='blue')

        ax.plot(angles, target_normalized, 'o-', linewidth=2, label='Целевой стиль', color='red')
        ax.fill(angles, target_normalized, alpha=0.15, color='red')

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics, fontsize=10)
        ax.set_ylim(0, 1.1)
        ax.set_title('Сравнение стилистических характеристик', fontsize=14, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        ax.grid(True)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig

    def generate_bar_chart(self,
                           deviation_analysis: Dict[str, Dict[str, float]],
                           save_path: Optional[str] = None) -> plt.Figure:
        """
        Generate bar chart showing metric deviations.

        Args:
            deviation_analysis (Dict): Deviation analysis
            save_path (str, optional): Path to save the chart

        Returns:
            plt.Figure: Generated figure
        """
        if not deviation_analysis:
            raise ValueError("No deviation analysis data provided")

        metrics = []
        current_values = []
        target_values = []
        colors = []

        for metric_name, analysis in deviation_analysis.items():
            metrics.append(self._format_metric_name(metric_name))
            current_values.append(analysis['current'])
            target_values.append(analysis['target'])

            colors.append('green' if analysis['within_tolerance'] else 'red')

        x = np.arange(len(metrics))
        width = 0.35

        fig, ax = plt.subplots(figsize=(12, 6))

        bars1 = ax.bar(x - width / 2, current_values, width, label='Текущий', color='blue')
        bars2 = ax.bar(x + width / 2, target_values, width, label='Цель', color='light gray')

        for i, (metric_name, analysis) in enumerate(deviation_analysis.items()):
            y_target = analysis['target']
            tolerance = analysis['tolerance']

            ax.plot([i + width / 2 - 0.1, i + width / 2 + 0.1],
                    [y_target - tolerance, y_target - tolerance],
                    'k-', linewidth=0.5)
            ax.plot([i + width / 2 - 0.1, i + width / 2 + 0.1],
                    [y_target + tolerance, y_target + tolerance],
                    'k-', linewidth=0.5)
            ax.plot([i + width / 2, i + width / 2],
                    [y_target - tolerance, y_target + tolerance],
                    'k-', linewidth=0.5)

        ax.set_xlabel('Метрики', fontsize=12)
        ax.set_ylabel('Значение', fontsize=12)
        ax.set_title('Отклонение от целевого стиля', fontsize=14)
        ax.set_xticks(x)
        ax.set_xticklabels(metrics, rotation=45, ha='right')
        ax.legend()

        for bar in bars1:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        return fig

    @staticmethod
    def _format_metric_name(metric_name: str) -> str:
        """Format metric name for display."""
        names = {
            'lexical_diversity': 'Лексическое\nразнообразие',
            'formality_score': 'Формальность',
            'readability_index': 'Удобочитаемость',
            'sentence_length_avg': 'Средняя длина\nпредложения',
            'word_length_avg': 'Средняя длина\nслова',
            'pos_frequency_NOUN': 'Частота\nсуществительных',
            'pos_frequency_VERB': 'Частота\nглаголов',
            'pos_frequency_ADJ': 'Частота\nприлагательных'
        }

        return names.get(metric_name, metric_name.replace('_', ' ').title())

    def generate_statistics_report(self,
                                   current_metrics: Dict[str, float],
                                   target_metrics: Dict[str, Any]) -> str:
        """
        Generate text statistics report.

        Args:
            current_metrics (Dict): Current metrics
            target_metrics (Dict): Target metrics configuration

        Returns:
            str: Text report
        """
        deviation = self.calculate_style_deviation(current_metrics, target_metrics)
        overall_score = self.calculate_overall_score(deviation)

        report_lines = [
            "СТАТИСТИЧЕСКИЙ АНАЛИЗ СТИЛЯ",
            "=" * 50,
            f"Общее соответствие стилю: {overall_score:.1%}",
            "",
            "ДЕТАЛЬНЫЙ АНАЛИЗ МЕТРИК:",
            "-" * 50
        ]

        for metric_name, analysis in deviation.items():
            status = "✓ В пределах нормы" if analysis['within_tolerance'] else "✗ Требует коррекции"
            diff_direction = "ниже" if analysis['current'] < analysis['target'] else "выше"

            report_lines.extend([
                f"\nМетрика: {self._format_metric_name(metric_name)}",
                f"  Текущее значение: {analysis['current']:.3f}",
                f"  Целевое значение: {analysis['target']:.3f}",
                f"  Отклонение: {analysis['absolute_diff']:.3f} ({analysis['relative_diff']:.1%}) {diff_direction}",
                f"  Допуск: ±{analysis['tolerance']:.3f}",
                f"  Статус: {status}",
                f"  Вес метрики: {analysis['weight']:.2f}"
            ])

        return "\n".join(report_lines)
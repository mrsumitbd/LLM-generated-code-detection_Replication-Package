from simpleval.commands.reporting.compare.common import CompareArgs
from simpleval.commands.reporting.compare.compare_console import _compare_results_console
from simpleval.commands.reporting.compare.compare_html2.compare_html2 import _compare_results_html2
from simpleval.consts import LOGGER_NAME, ReportFormat

def _compare_results_report(eval_set: str, left_side: CompareArgs, right_side: CompareArgs, output_format: str):
    if output_format == ReportFormat.CONSOLE:
        _compare_results_console(left_side=left_side, right_side=right_side)
    elif output_format == ReportFormat.HTML:
        _compare_results_html2(eval_set=eval_set, left_side=left_side, right_side=right_side)
    else:
        raise ValueError(f'Invalid report format: {output_format}')
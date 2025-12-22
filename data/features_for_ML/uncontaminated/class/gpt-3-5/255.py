from typing import Dict, Any, List
from pathlib import Path

class ParallelJsonDumper:

    def __init__(self, parallel_field: str, chunk_size: int = 5000):
        self.parallel_field = parallel_field
        self.chunk_size = chunk_size

    def dump(self, data: Dict[str, Any], output_path: Path) -> None:
        base_data = data.copy()
        del base_data[self.parallel_field]

        pvalue = data[self.parallel_field]
        chunked_values = self._chunkify_list(pvalue)

        chunk_strings = []
        for chunk in chunked_values:
            chunk_str = self._process_chunk(chunk)
            chunk_strings.append(chunk_str)

        self._write_output(base_data, chunk_strings, output_path)

    def _chunkify_list(self, pvalue: List[Any]) -> List[List[Any]]:
        return [pvalue[i:i + self.chunk_size] for i in range(0, len(pvalue), self.chunk_size)]

    def _process_chunk(self, chunk: List[Any]) -> str:
        return "[" + ", ".join(str(item) for item in chunk) + "]"

    def _write_output(self, base_data: Dict[str, Any], chunk_strings: List[str], output_path: Path) -> None:
        with open(output_path, 'w') as file:
            for chunk_str in chunk_strings:
                file.write(str(base_data) + ", " + chunk_str + "\n")
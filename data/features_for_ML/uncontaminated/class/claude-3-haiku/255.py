import json
from pathlib import Path
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor

class ParallelJsonDumper:

    def __init__(self, parallel_field: str, chunk_size: int = 5000):
        self.parallel_field = parallel_field
        self.chunk_size = chunk_size

    def dump(self, data: Dict[str, Any], output_path: Path) -> None:
        parallel_data = data[self.parallel_field]
        chunks = self._chunkify_list(parallel_data)

        with ThreadPoolExecutor() as executor:
            chunk_strings = list(executor.map(self._process_chunk, chunks))

        self._write_output(data, chunk_strings, output_path)

    def _chunkify_list(self, pvalue: List[Any]) -> List[List[Any]]:
        return [pvalue[i:i+self.chunk_size] for i in range(0, len(pvalue), self.chunk_size)]

    def _process_chunk(self, chunk: List[Any]) -> str:
        return json.dumps(chunk)

    def _write_output(self, base_data: Dict[str, Any], chunk_strings: List[str], output_path: Path) -> None:
        with open(output_path, 'w') as f:
            base_data[self.parallel_field] = chunk_strings
            json.dump(base_data, f)
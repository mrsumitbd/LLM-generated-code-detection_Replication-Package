from typing import Dict, Any, List
from pathlib import Path
import json
from multiprocessing import Pool
import os


class ParallelJsonDumper:

    def __init__(self, parallel_field: str, chunk_size: int = 5000):
        self.parallel_field = parallel_field
        self.chunk_size = chunk_size

    def dump(self, data: Dict[str, Any], output_path: Path) -> None:
        if self.parallel_field not in data:
            with open(output_path, 'w') as f:
                json.dump(data, f)
            return

        pvalue = data[self.parallel_field]
        if not isinstance(pvalue, list):
            with open(output_path, 'w') as f:
                json.dump(data, f)
            return

        chunks = self._chunkify_list(pvalue)
        
        num_workers = os.cpu_count() or 1
        with Pool(num_workers) as pool:
            chunk_strings = pool.map(self._process_chunk, chunks)
        
        base_data = {k: v for k, v in data.items() if k != self.parallel_field}
        self._write_output(base_data, chunk_strings, output_path)

    def _chunkify_list(self, pvalue: List[Any]) -> List[List[Any]]:
        chunks = []
        for i in range(0, len(pvalue), self.chunk_size):
            chunks.append(pvalue[i:i + self.chunk_size])
        return chunks

    def _process_chunk(self, chunk: List[Any]) -> str:
        return json.dumps(chunk)

    def _write_output(self, base_data: Dict[str, Any], chunk_strings: List[str], output_path: Path) -> None:
        with open(output_path, 'w') as f:
            f.write('{')
            
            first = True
            for key, value in base_data.items():
                if not first:
                    f.write(',')
                f.write(json.dumps(key))
                f.write(':')
                f.write(json.dumps(value))
                first = False
            
            if not first:
                f.write(',')
            f.write(json.dumps(self.parallel_field))
            f.write(':[')
            
            for i, chunk_str in enumerate(chunk_strings):
                if i > 0:
                    f.write(',')
                f.write(chunk_str[1:-1])
            
            f.write(']}')
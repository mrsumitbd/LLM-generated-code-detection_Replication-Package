import json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from typing import Dict, Any, List


class ParallelJsonDumper:
    def __init__(self, parallel_field: str, chunk_size: int = 5000):
        """
        Initialize the dumper.

        :param parallel_field: The key in the data dict that contains the list to be processed in parallel.
        :param chunk_size: Number of items per chunk.
        """
        self.parallel_field = parallel_field
        self.chunk_size = chunk_size

    def dump(self, data: Dict[str, Any], output_path: Path) -> None:
        """
        Dump the data to a JSON file, processing the specified list in parallel chunks.

        :param data: The source dictionary.
        :param output_path: Path to write the JSON output.
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")

        if self.parallel_field not in data:
            raise KeyError(f"'{self.parallel_field}' not found in data")

        # Extract the list to be processed
        pvalue = data.pop(self.parallel_field)
        if not isinstance(pvalue, list):
            raise TypeError(f"'{self.parallel_field}' must be a list")

        # Split into chunks
        chunks = self._chunkify_list(pvalue)

        # Process chunks in parallel
        with ProcessPoolExecutor() as executor:
            chunk_strings = list(executor.map(self._process_chunk, chunks))

        # Write the final output
        self._write_output(data, chunk_strings, output_path)

    def _chunkify_list(self, pvalue: List[Any]) -> List[List[Any]]:
        """
        Split a list into smaller chunks.

        :param pvalue: The list to split.
        :return: A list of list chunks.
        """
        return [
            pvalue[i : i + self.chunk_size]
            for i in range(0, len(pvalue), self.chunk_size)
        ]

    def _process_chunk(self, chunk: List[Any]) -> str:
        """
        Process a single chunk. Here we simply JSON-serialize it.

        :param chunk: The chunk to process.
        :return: JSON string representation of the chunk.
        """
        return json.dumps(chunk, ensure_ascii=False)

    def _write_output(
        self, base_data: Dict[str, Any], chunk_strings: List[str], output_path: Path
    ) -> None:
        """
        Combine processed chunks and write the final JSON file.

        :param base_data: The original data dictionary without the parallel field.
        :param chunk_strings: List of JSON strings for each chunk.
        :param output_path: Path to write the JSON output.
        """
        # Reconstruct the full list from chunk strings
        full_list: List[Any] = []
        for chunk_str in chunk_strings:
            full_list.extend(json.loads(chunk_str))

        # Insert the reconstructed list back into the data
        base_data[self.parallel_field] = full_list

        # Write to file
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(base_data, f, ensure_ascii=False, indent=2)
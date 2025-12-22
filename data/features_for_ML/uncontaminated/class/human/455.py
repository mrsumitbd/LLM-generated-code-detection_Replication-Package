import h5py
import numpy as np
from pathlib import Path
import datasets
from .dataclasses import Equation, Problem

class TransformedFeynmanDataModule:
    def __init__(self):
        self._dataset_dir = None
        self._dataset_identifier = "lsr_transform"

    def setup(self):
        self._dataset_dir = Path(_download(repo_id=REPO_ID))
        ds = datasets.load_dataset(REPO_ID)["lsr_transform"]
        sample_h5file_path = self._dataset_dir / "lsr_bench_data.hdf5"
        self.problems = []
        with h5py.File(sample_h5file_path, "r") as sample_file:
            for e in ds:
                samples = {
                    k: v[...].astype(np.float64)
                    for k, v in sample_file[f'/lsr_transform/{e["name"]}'].items()
                }
                self.problems.append(
                    Problem(
                        dataset_identifier=self._dataset_identifier,
                        equation_idx=e["name"],
                        gt_equation=Equation(
                            symbols=e["symbols"],
                            symbol_descs=e["symbol_descs"],
                            symbol_properties=e["symbol_properties"],
                            expression=e["expression"],
                        ),
                        samples=samples,
                    )
                )
        self.name2id = {p.equation_idx: i for i, p in enumerate(self.problems)}

    @property
    def name(self):
        return "LSR_Transform"
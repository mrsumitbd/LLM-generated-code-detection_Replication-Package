import os
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Tuple, Dict, Any

class SyntenicPlot:
    """Syntenic plots between CGCs and PULs"""

    def __init__(self, config: Any):
        """
        Parameters
        ----------
        config : SynPlotConfig
            Configuration object containing paths and options.
        """
        self.config = config
        self.cgc_gff = self._read_gff(config.cgc_gff_path)
        self.pul_gff = self._read_gff(config.pul_gff_path)
        self.output_dir = config.output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _read_gff(self, path: str) -> pd.DataFrame:
        """Read a GFF file into a DataFrame."""
        cols = ["seqid", "source", "type", "start", "end", "score",
                "strand", "phase", "attributes"]
        df = pd.read_csv(path, sep="\t", comment="#", header=None, names=cols,
                         dtype={"start": int, "end": int, "strand": str})
        return df

    def read_PUL_cgcgff(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Return the CGC and PUL GFF DataFrames."""
        return self.cgc_gff, self.pul_gff

    def syntenic_plot_allpairs(self):
        """Generate syntenic plots for all CGC–PUL pairs."""
        for _, cgc_row in self.cgc_gff.iterrows():
            cgcid = self._parse_attribute(cgc_row["attributes"], "ID")
            substrate = self._parse_attribute(cgc_row["attributes"], "substrate")
            for _, pul_row in self.pul_gff.iterrows():
                pulid = self._parse_attribute(pul_row["attributes"], "ID")
                self._create_syntenic_plot(
                    starts=[cgc_row["start"]],
                    starts1=[pul_row["start"]],
                    ends=[cgc_row["end"]],
                    ends1=[pul_row["end"]],
                    strands=[cgc_row["strand"]],
                    strands1=[pul_row["strand"]],
                    types=[cgc_row["type"]],
                    types1=[pul_row["type"]],
                    blocks=[(cgc_row["start"], cgc_row["end"], pul_row["start"], pul_row["end"])],
                    cgcid=cgcid,
                    pulid=pulid,
                    substrate=substrate,
                )

    def _parse_attribute(self, attr_str: str, key: str) -> str:
        """Parse a GFF attribute string for a given key."""
        for part in attr_str.split(";"):
            if part.strip().startswith(f"{key}="):
                return part.split("=", 1)[1]
        return ""

    def _create_syntenic_plot(
        self,
        starts: List[int],
        starts1: List[int],
        ends: List[int],
        ends1: List[int],
        strands: List[str],
        strands1: List[str],
        types: List[str],
        types1: List[str],
        blocks: List[Tuple[int, int, int, int]],
        cgcid: str,
        pulid: str,
        substrate: str,
    ):
        """Create a simple syntenic plot for one CGC–PUL pair."""
        fig, ax = plt.subplots(figsize=(8, 4))
        # Plot CGC line
        ax.hlines(1, min(starts), max(ends), colors="blue", linewidth=5, label="CGC")
        # Plot PUL line
        ax.hlines(2, min(starts1), max(ends1), colors="red", linewidth=5, label="PUL")
        # Draw blocks
        for (s1, e1, s2, e2) in blocks:
            ax.plot([s1, s2], [1, 2], color="gray", linewidth=1)
        # Formatting
        ax.set_ylim(0.5, 2.5)
        ax.set_yticks([1, 2])
        ax.set_yticklabels(["CGC", "PUL"])
        ax.set_xlabel("Genomic coordinate")
        ax.set_title(f"Synteny: {cgcid} vs {pulid} ({substrate})")
        ax.legend()
        # Save figure
        out_path = os.path.join(
            self.output_dir, f"{cgcid}_{pulid}_{substrate}.png"
        )
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.close(fig)
import pandas as pd
import numpy as np
from typing import Sequence, Dict, List, Optional
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests

# Constants (these would normally be defined elsewhere)
MIN_GENESET_SIZE = 5
MAX_GENESET_SIZE = 500

def de_enrichment_analysis(
    de_results: pd.DataFrame,
    group_key: str = "group",
    effect_key: str = "log2fc",
    pval_key: str = "padj",
    feature_key: str = "feature",
    effect_thresh: float = 0.5,
    pval_thresh: float = 0.01,
    gene_sets: Optional[Dict[str, List[str]]] = None,
    top_n: Optional[int] = None,
    background: Optional[Sequence[str]] = None,
    collection: str = "all",
    url: Optional[str] = None,
    filepath: Optional[str] = None,
    geneset_key: str = "geneset",
    genesymbol_key: str = "genesymbol",
    method: str = "enrichr",
    cutoff: float = 0.05,
    min_genes: int = MIN_GENESET_SIZE,
    max_genes: int = MAX_GENESET_SIZE,
) -> pd.DataFrame:
    """
    Run enrichment for up/down gene sets per group and stack filtered results.
    Uses get_de_genes to extract significant genes based on thresholds.
    """
    # ------------------------------------------------------------------
    # Helper: get DE genes for a group and direction
    # ------------------------------------------------------------------
    def _get_de_genes(df: pd.DataFrame, grp: str, direction: str) -> List[str]:
        sub = df[df[group_key] == grp]
        # Filter by thresholds
        mask = (
            (sub[effect_key].abs() >= effect_thresh)
            & (sub[pval_key] <= pval_thresh)
        )
        sub = sub[mask]
        if direction == "up":
            sub = sub[sub[effect_key] > 0]
        elif direction == "down":
            sub = sub[sub[effect_key] < 0]
        else:
            raise ValueError("direction must be 'up' or 'down'")
        # Optional top_n
        if top_n is not None:
            sub = sub.assign(abs_effect=sub[effect_key].abs())
            sub = sub.sort_values("abs_effect", ascending=False).head(top_n)
        return sub[feature_key].tolist()

    # ------------------------------------------------------------------
    # Load gene sets if not provided
    # ------------------------------------------------------------------
    if gene_sets is None:
        raise ValueError("gene_sets must be provided or loaded from a source")

    # Filter gene sets by size
    filtered_gene_sets = {
        gs: [g for g in genes if g in background or background is None]
        for gs, genes in gene_sets.items()
        if min_genes <= len(genes) <= max_genes
    }

    # Determine background if not provided
    if background is None:
        background = set()
        for genes in filtered_gene_sets.values():
            background.update(genes)
        background = list(background)

    # ------------------------------------------------------------------
    # Perform enrichment per group and direction
    # ------------------------------------------------------------------
    results = []

    for grp in de_results[group_key].unique():
        for direction in ("up", "down"):
            de_genes = set(_get_de_genes(de_results, grp, direction))
            if not de_genes:
                continue

            # Prepare p-values list for multiple testing correction
            pvals = []
            gene_set_names = []
            overlaps = []

            for gs_name, gs_genes in filtered_gene_sets.items():
                gs_set = set(gs_genes)
                overlap = de_genes & gs_set
                if not overlap:
                    pvals.append(1.0)
                    gene_set_names.append(gs_name)
                    overlaps.append([])
                    continue

                # Build contingency table
                a = len(overlap)
                b = len(de_genes) - a
                c = len(gs_set) - a
                d = len(background) - (a + b + c)
                # Fisher exact test (two-sided)
                _, p = fisher_exact([[a, b], [c, d]], alternative="two-sided")
                pvals.append(p)
                gene_set_names.append(gs_name)
                overlaps.append(list(overlap))

            # Multiple testing correction
            _, adj_pvals, _, _ = multipletests(pvals, alpha=cutoff, method="fdr_bh")

            # Compile results
            for gs_name, adj_p, ov in zip(gene_set_names, adj_pvals, overlaps):
                if adj_p <= cutoff:
                    results.append(
                        {
                            geneset_key: gs_name,
                            genesymbol_key: ", ".join(ov),
                            "Adjusted P-value": adj_p,
                            "up_dw": direction,
                            group_key: grp,
                        }
                    )

    return pd.DataFrame(results)
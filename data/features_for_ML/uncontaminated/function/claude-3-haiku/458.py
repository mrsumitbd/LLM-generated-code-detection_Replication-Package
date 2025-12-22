import pandas as pd
from typing import Sequence, Tuple
from collections import defaultdict
from functools import partial
from enrichr import Enrichr

MIN_GENESET_SIZE = 3
MAX_GENESET_SIZE = 500

def get_de_genes(
    df: pd.DataFrame,
    effect_key: str,
    pval_key: str,
    effect_thresh: float,
    pval_thresh: float,
    top_n: int | None = None,
) -> Tuple[dict[str, list[str]], dict[str, list[str]]]:
    """
    Extract significant up- and down-regulated genes based on effect size and p-value thresholds.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing differential expression results.
    effect_key : str
        Column with effect size values for DE analysis.
    pval_key : str
        Column with p-values for DE analysis.
    effect_thresh : float
        Threshold for absolute effect size.
    pval_thresh : float
        Threshold for significance of DE genes.
    top_n : int, optional
        If specified, only consider the top N genes per group for enrichment analysis.

    Returns
    -------
    Tuple[dict[str, list[str]], dict[str, list[str]]]
        Dictionaries of up- and down-regulated genes, keyed by group.
    """
    up_genes = defaultdict(list)
    down_genes = defaultdict(list)

    for group, group_df in df.groupby(group_key):
        group_df = group_df.sort_values(abs(effect_key), ascending=False)
        if top_n:
            group_df = group_df.head(top_n)

        up_mask = (group_df[effect_key] > effect_thresh) & (group_df[pval_key] < pval_thresh)
        down_mask = (group_df[effect_key] < -effect_thresh) & (group_df[pval_key] < pval_thresh)

        up_genes[group] = group_df.loc[up_mask, feature_key].tolist()
        down_genes[group] = group_df.loc[down_mask, feature_key].tolist()

    return up_genes, down_genes

def de_enrichment_analysis(
    de_results: pd.DataFrame,
    group_key: str = "group",
    effect_key: str = "log2fc",
    pval_key: str = "padj",
    feature_key: str = "feature",
    effect_thresh: float = 0.5,
    pval_thresh: float = 0.01,
    gene_sets: dict[str, list[str]] | None = None,
    top_n: int | None = None,
    background: Sequence[str] | None = None,
    collection: str = "all",
    url: str | None = None,
    filepath: str | None = None,
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

    Parameters
    ...
    """
    up_genes, down_genes = get_de_genes(
        de_results, effect_key, pval_key, effect_thresh, pval_thresh, top_n
    )

    enrichr = Enrichr(gene_sets=gene_sets, background=background, collection=collection, url=url, filepath=filepath)

    results = []
    for group, up_set in up_genes.items():
        up_enrichment = enrichr.enrich(up_set, method=method, cutoff=cutoff, min_genes=min_genes, max_genes=max_genes)
        up_enrichment["up_dw"] = "up"
        up_enrichment["group"] = group
        results.append(up_enrichment)

    for group, down_set in down_genes.items():
        down_enrichment = enrichr.enrich(down_set, method=method, cutoff=cutoff, min_genes=min_genes, max_genes=max_genes)
        down_enrichment["up_dw"] = "down"
        down_enrichment["group"] = group
        results.append(down_enrichment)

    enrichment_results = pd.concat(results)
    enrichment_results = enrichment_results[[geneset_key, genesymbol_key, "Adjusted P-value", "up_dw", "group"]]
    return enrichment_results
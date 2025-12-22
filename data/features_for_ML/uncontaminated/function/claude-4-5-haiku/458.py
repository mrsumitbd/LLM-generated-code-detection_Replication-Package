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
    """
    import gseapy as gp
    from gseapy.utils import load_gmt
    
    # Load gene sets if not provided
    if gene_sets is None:
        if filepath is not None:
            gene_sets = load_gmt(filepath)
        elif url is not None:
            gene_sets = load_gmt(url)
        else:
            gene_sets = gp.get_library(collection)
    
    # Filter gene sets by size
    gene_sets = {
        name: genes
        for name, genes in gene_sets.items()
        if min_genes <= len(genes) <= max_genes
    }
    
    # Get background genes if not provided
    if background is None:
        background = list(set(g for genes in gene_sets.values() for g in genes))
    
    results_list = []
    
    # Get unique groups
    groups = de_results[group_key].unique()
    
    for group in groups:
        group_data = de_results[de_results[group_key] == group].copy()
        
        # Get upregulated genes
        up_genes = get_de_genes(
            group_data,
            effect_key=effect_key,
            pval_key=pval_key,
            feature_key=feature_key,
            effect_thresh=effect_thresh,
            pval_thresh=pval_thresh,
            direction="up",
            top_n=top_n,
        )
        
        # Get downregulated genes
        down_genes = get_de_genes(
            group_data,
            effect_key=effect_key,
            pval_key=pval_key,
            feature_key=feature_key,
            effect_thresh=effect_thresh,
            pval_thresh=pval_thresh,
            direction="down",
            top_n=top_n,
        )
        
        # Run enrichment for upregulated genes
        if len(up_genes) > 0:
            if method == "enrichr":
                enr_up = gp.enrichr(
                    gene_list=up_genes,
                    gene_sets=gene_sets,
                    background=background,
                    cutoff=cutoff,
                )
                if enr_up.results is not None and len(enr_up.results) > 0:
                    enr_up_df = enr_up.results.copy()
                    enr_up_df["up_dw"] = "up"
                    enr_up_df["group"] = group
                    enr_up_df = enr_up_df.rename(
                        columns={"Term": geneset_key, "Genes": genesymbol_key}
                    )
                    results_list.append(enr_up_df)
        
        # Run enrichment for downregulated genes
        if len(down_genes) > 0:
            if method == "enrichr":
                enr_down = gp.enrichr(
                    gene_list=down_genes,
                    gene_sets=gene_sets,
                    background=background,
                    cutoff=cutoff,
                )
                if enr_down.results is not None and len(enr_down.results) > 0:
                    enr_down_df = enr_down.results.copy()
                    enr_down_df["up_dw"] = "down"
                    enr_down_df["group"] = group
                    enr_down_df = enr_down_df.rename(
                        columns={"Term": geneset_key, "Genes": genesymbol_key}
                    )
                    results_list.append(enr_down_df)
    
    # Combine results
    if len(results_list) > 0:
        combined_results = pd.concat(results_list, ignore_index=True)
        # Filter by cutoff on adjusted p-value
        combined_results = combined_results[
            combined_results["Adjusted P-value"] <= cutoff
        ]
        return combined_results
    else:
        return pd.DataFrame()
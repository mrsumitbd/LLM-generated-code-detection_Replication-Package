from pathlib import Path
import logging
from typing import Dict, Tuple, List
from dbcan.configs.cgc_substrate_config import SynPlotConfig
import dbcan.constants.plots_constants as plots_constants

class SyntenicPlot:
    """Syntenic plots between CGCs and PULs"""

    def __init__(self, config: SynPlotConfig):
        self.config = config
        self.output_dir = Path(config.output_dir).resolve()
        self.db_dir = Path(config.db_dir).resolve()

        self.input_sub_out = self.output_dir / plots_constants.CGC_SUB_PREDICTION_FILE
        self.blastp = self.output_dir / plots_constants.PUL_DIAMOND_FILE
        self.cgc = self.output_dir / plots_constants.CGC_RESULT_FILE

        fallback_sub = self.output_dir / "substrate_prediction.tsv"
        if (not self.input_sub_out.exists()) and fallback_sub.exists():
            logging.warning(f"[substrate] {self.input_sub_out.name} not found, using fallback file: {fallback_sub.name}")
            self.input_sub_out = fallback_sub

        self.pdf_dir = self.output_dir / "synteny_pdf"
        self.pdf_dir.mkdir(parents=True, exist_ok=True)

        logging.info(f"[synteny init] output_dir={self.output_dir}")
        logging.info(f"[synteny init] substrate_file={self.input_sub_out} (exists={self.input_sub_out.exists()})")
        logging.info(f"[synteny init] blast_file={self.blastp} (exists={self.blastp.exists()})")
        logging.info(f"[synteny init] cgc_file={self.cgc} (exists={self.cgc.exists()})")
        logging.info(f"[synteny init] dbCAN-PUL dir={self.db_dir / 'dbCAN-PUL'} (exists={(self.db_dir / 'dbCAN-PUL').is_dir()})")

    def syntenic_plot_allpairs(self):
        """overall function to plot all CGC-PUL pairs"""
        if not self.blastp.exists() or self.blastp.stat().st_size == 0:
            logger.warning(f"[skip] BLAST result not found or empty: {self.blastp}")
            return
        cgcpul_blastp = read_blast_result_cgc(str(self.blastp))
        logging.info(f"[load] BLAST pair groups: {len(cgcpul_blastp)}")

        if not self.cgc.exists():
            logger.error(f"[abort] CGC standard out not found: {self.cgc}")
            return
        cgc_proteinid2gene, cgcid2gene, cgcid2geneid = read_UHGG_CGC_stanrdard_out(str(self.cgc))
        logging.info(f"[load] CGC IDs: {len(cgcid2gene)} (proteins={len(cgc_proteinid2gene)})")

        PULid_proteinid2gene, PULid2gene, PULid2geneid = self.read_PUL_cgcgff()
        logging.info(f"[load] PUL IDs: {len(PULid2gene)} (proteins={len(PULid_proteinid2gene)})")

        if not self.input_sub_out.exists() or self.input_sub_out.stat().st_size == 0:
            logger.warning(f"[skip] Substrate prediction file not found or empty: {self.input_sub_out}")
            return

        plot_count = 0
        candidate_pairs = 0
        no_blast_pairs = 0
        missing_cgc = 0
        missing_pul = 0

        with self.input_sub_out.open() as fh:
            header = next(fh, "")
            for line in fh:
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 2:
                    continue
                cgc, pul = parts[0].strip(), parts[1].strip()
                substrate = parts[2].strip() if len(parts) > 2 else ""
                if not pul:
                    continue
                candidate_pairs += 1

                if cgc not in cgcid2gene:
                    missing_cgc += 1
                    logger.debug(f"[miss CGC] {cgc} not in cgc_standard_out")
                    continue
                if pul not in PULid2gene:
                    missing_pul += 1
                    logger.debug(f"[miss PUL] {pul} not in PUL gff db")
                    continue

                cgcpul_key = f"{cgc}:{pul}"

                bed_cgc = cgcid2gene[cgc]
                bed_pul = PULid2gene[pul]

                starts1, ends1, strands1, types1 = Get_parameters_for_plot(bed_cgc)
                starts2, ends2, strands2, types2 = Get_parameters_for_plot(bed_pul)
                genes1 = cgcid2geneid[cgc]
                genes2 = PULid2geneid[pul]

                blocks = []
                if cgcpul_key in cgcpul_blastp:
                    for rec in cgcpul_blastp[cgcpul_key]:
                        qseqid = rec.qseqid
                        sseqid = rec.sseqid
                        try:
                            cgc_proteinid = qseqid.split("|")[2]
                        except Exception:
                            continue
                        _, pul_proteinid = parse_pul_ids(sseqid)
                        try:
                            idx1 = genes1.index(cgc_proteinid)
                            idx2 = genes2.index(pul_proteinid)
                            blocks.append(f"{idx1}-{idx2}-{rec.pident}")
                        except ValueError:
                            continue
                else:
                    no_blast_pairs += 1
                    logger.debug(f"[no BLAST] {cgcpul_key} no alignment blocks; plotting empty synteny")

                self._create_syntenic_plot(
                    starts1, starts2, ends1, ends2,
                    strands1, strands2, types1, types2,
                    blocks, cgc, pul, substrate
                )
                plot_count += 1

        if plot_count == 0:
            logger.warning(
                "[diagnostic]error candidate=%d, blast_groups=%d, CGC=%d, PUL=%d. "
                "missing_cgc=%d, missing_pul=%d, no_blast=%d",
                candidate_pairs, len(cgcpul_blastp), len(cgcid2gene), len(PULid2gene),
                missing_cgc, missing_pul, no_blast_pairs
            )
        else:
            logger.info(
                "Generated %d syntenic plots (candidate=%d, missing_cgc=%d, missing_pul=%d, no_blast=%d)",
                plot_count, candidate_pairs, missing_cgc, missing_pul, no_blast_pairs
            )

    def read_PUL_cgcgff(self):
        """
        Read PUL cgc.gff files to get gene annotations.
        """
        PULidgeneid2gene: Dict[str, CGC_stanrdard] = {}
        pul_dir = self.db_dir / "dbCAN-PUL"
        if not pul_dir.is_dir():
            logger.warning(f"dbCAN-PUL directory not found: {pul_dir}")
            return {}, {}, {}

        for entry in pul_dir.iterdir():
            if entry.is_dir() and entry.name.startswith("PUL") and entry.name.endswith(".out"):
                gff_path = entry / "cgc.gff"
                read_cgcgff(gff_path, PULidgeneid2gene)

        cgcid2gene: Dict[str, List[CGC_stanrdard]] = {}
        cgcid2geneid: Dict[str, List[str]] = {}
        for PULidgeneid, gene in PULidgeneid2gene.items():
            cgcid2gene.setdefault(gene.CGCID, []).append(gene)
            cgcid2geneid.setdefault(gene.CGCID, []).append(gene.Protein_ID)

        return PULidgeneid2gene, cgcid2gene, cgcid2geneid

    def _create_syntenic_plot(self, starts, starts1, ends, ends1, strands, strands1, types, types1, blocks, cgcid, pulid, substrate):
        plot_config = {'output_dir': self.output_dir}
        syntenic_plot(starts, starts1, ends, ends1, strands, strands1,
                      types, types1, blocks, cgcid, pulid, substrate, plot_config)
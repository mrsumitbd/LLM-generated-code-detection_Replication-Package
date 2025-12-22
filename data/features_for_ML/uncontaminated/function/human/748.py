import os
from dbcan.process.process_utils import (
        process_cgc_null_pfam_annotation,
        extract_null_fasta_from_cgc,
        annotate_cgc_null_with_pfam_and_gff,
        extract_null_fasta_from_gff
    )
from dbcan.annotation.pyhmmer_search import PyHMMERPfamProcessor

def run_dbCAN_Pfam_null_cgc(config):
    from dbcan.process.process_utils import (
        process_cgc_null_pfam_annotation,
        extract_null_fasta_from_cgc,
        annotate_cgc_null_with_pfam_and_gff,
        extract_null_fasta_from_gff
    )
    from dbcan.annotation.pyhmmer_search import PyHMMERPfamProcessor

    # choose the source of null genes
    if getattr(config, 'null_from_gff', False):
        extract_null_fasta_from_gff(
            os.path.join(config.output_dir, 'cgc.gff'),
            os.path.join(config.output_dir, 'uniInput.faa'),
            os.path.join(config.output_dir, 'null_proteins.faa')
        )
    else:
        extract_null_fasta_from_cgc(
            os.path.join(config.output_dir, 'cgc_standard_out.tsv'),
            os.path.join(config.output_dir, 'uniInput.faa'),
            os.path.join(config.output_dir, 'null_proteins.faa')
        )

    pfam_processor = PyHMMERPfamProcessor(config)
    pfam_processor.run()
    process_cgc_null_pfam_annotation(config)
    annotate_cgc_null_with_pfam_and_gff(
        os.path.join(config.output_dir, 'cgc_standard_out.tsv'),
        os.path.join(config.output_dir, 'Pfam_hmm_results.tsv'),
        os.path.join(config.output_dir, 'cgc.gff'),
        os.path.join(config.output_dir, 'cgc_standard_out.pfam_annotated.tsv'),
        os.path.join(config.output_dir, 'cgc.pfam_annotated.gff')
    )
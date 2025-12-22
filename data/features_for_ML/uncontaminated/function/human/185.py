import rich_click as click

def cgc_gff_option(func):
    func = click.option('--input_gff', required=True, help='input GFF file')(func)
    func = click.option('--gff_type', required=True, help='GFF file type')(func)
    return func
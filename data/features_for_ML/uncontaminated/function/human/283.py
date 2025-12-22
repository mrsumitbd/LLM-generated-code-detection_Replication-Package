import rich_click as click

def diamond_peptidase_options(func):
    func = click.option('--e_value_threshold_peptidase', type=float, help='E-value threshold for Peptidase', default=1e-4)(func)
    func = click.option('--coverage_threshold_peptidase', type=float, help='Coverage threshold for Peptidase', default=0.35)(func)
    return func
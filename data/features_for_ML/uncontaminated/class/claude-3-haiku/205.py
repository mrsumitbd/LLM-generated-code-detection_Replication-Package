class SyntenicPlot:
    """Syntenic plots between CGCs and PULs"""

    def __init__(self, config: SynPlotConfig):
        self.config = config
        self.cgc_gff = None
        self.pul_gff = None
        self.cgc_pul_pairs = []

    def syntenic_plot_allpairs(self):
        self.read_PUL_cgcgff()
        for cgc, pul in self.cgc_pul_pairs:
            self._create_syntenic_plot(
                self.cgc_gff[cgc]['starts'],
                self.pul_gff[pul]['starts'],
                self.cgc_gff[cgc]['ends'],
                self.pul_gff[pul]['ends'],
                self.cgc_gff[cgc]['strands'],
                self.pul_gff[pul]['strands'],
                self.cgc_gff[cgc]['types'],
                self.pul_gff[pul]['types'],
                self.config.block_size,
                cgc,
                pul,
                self.config.substrate
            )

    def read_PUL_cgcgff(self):
        self.cgc_gff = read_gff(self.config.cgc_gff_path)
        self.pul_gff = read_gff(self.config.pul_gff_path)
        self.cgc_pul_pairs = find_cgc_pul_pairs(self.cgc_gff, self.pul_gff, self.config.max_distance)

    def _create_syntenic_plot(self, starts, starts1, ends, ends1, strands, strands1, types, types1, blocks, cgcid, pulid, substrate):
        # Implementation of the _create_syntenic_plot method
        pass
class SyntenicPlot:
    """Syntenic plots between CGCs and PULs"""

    def __init__(self, config: SynPlotConfig):
        self.config = config
        self.pul_data = {}
        self.cgc_data = {}
        self.output_dir = config.output_dir
        self.min_identity = config.min_identity if hasattr(config, 'min_identity') else 0.0
        self.min_coverage = config.min_coverage if hasattr(config, 'min_coverage') else 0.0

    def syntenic_plot_allpairs(self):
        """Generate syntenic plots for all CGC-PUL pairs"""
        self.read_PUL_cgcgff()
        
        for cgc_id, cgc_info in self.cgc_data.items():
            for pul_id, pul_info in self.pul_data.items():
                self._create_syntenic_plot(
                    cgc_info['starts'],
                    pul_info['starts'],
                    cgc_info['ends'],
                    pul_info['ends'],
                    cgc_info['strands'],
                    pul_info['strands'],
                    cgc_info['types'],
                    pul_info['types'],
                    cgc_info.get('blocks', []),
                    cgc_id,
                    pul_id,
                    cgc_info.get('substrate', 'unknown')
                )

    def read_PUL_cgcgff(self):
        """Read PUL and CGC GFF files"""
        if hasattr(self.config, 'pul_gff') and self.config.pul_gff:
            self._parse_gff(self.config.pul_gff, self.pul_data)
        
        if hasattr(self.config, 'cgc_gff') and self.config.cgc_gff:
            self._parse_gff(self.config.cgc_gff, self.cgc_data)

    def _parse_gff(self, gff_file, data_dict):
        """Parse GFF file and populate data dictionary"""
        try:
            with open(gff_file, 'r') as f:
                current_id = None
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split('\t')
                    if len(parts) < 9:
                        continue
                    
                    seqid, source, feature_type, start, end, score, strand, phase, attributes = parts
                    
                    attr_dict = {}
                    for attr in attributes.split(';'):
                        if '=' in attr:
                            key, value = attr.split('=', 1)
                            attr_dict[key] = value
                    
                    feature_id = attr_dict.get('ID', attr_dict.get('Parent', seqid))
                    
                    if feature_id not in data_dict:
                        data_dict[feature_id] = {
                            'starts': [],
                            'ends': [],
                            'strands': [],
                            'types': [],
                            'blocks': [],
                            'substrate': attr_dict.get('substrate', 'unknown')
                        }
                    
                    data_dict[feature_id]['starts'].append(int(start))
                    data_dict[feature_id]['ends'].append(int(end))
                    data_dict[feature_id]['strands'].append(strand)
                    data_dict[feature_id]['types'].append(feature_type)
        except FileNotFoundError:
            pass

    def _create_syntenic_plot(self, starts, starts1, ends, ends1, strands, strands1, types, types1, blocks, cgcid, pulid, substrate):
        """Create a syntenic plot for a CGC-PUL pair"""
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        y_pos_cgc = 2
        y_pos_pul = 1
        
        max_end_cgc = max(ends) if ends else 0
        max_end_pul = max(ends1) if ends1 else 0
        max_end = max(max_end_cgc, max_end_pul)
        
        for i, (start, end, strand, ftype) in enumerate(zip(starts, ends, strands, types)):
            color = self._get_color_by_type(ftype)
            width = end - start
            
            if strand == '+':
                arrow = FancyArrowPatch((start, y_pos_cgc - 0.3), (end, y_pos_cgc - 0.3),
                                       arrowstyle='->', mutation_scale=20, color=color, linewidth=2)
            else:
                arrow = FancyArrowPatch((end, y_pos_cgc - 0.3), (start, y_pos_cgc - 0.3),
                                       arrowstyle='->', mutation_scale=20, color=color, linewidth=2)
            ax.add_patch(arrow)
        
        for i, (start, end, strand, ftype) in enumerate(zip(starts1, ends1, strands1, types1)):
            color = self._get_color_by_type(ftype)
            
            if strand == '+':
                arrow = FancyArrowPatch((start, y_pos_pul - 0.3), (end, y_pos_pul - 0.3),
                                       arrowstyle='->', mutation_scale=20, color=color, linewidth=2)
            else:
                arrow = FancyArrowPatch((end, y_pos_pul - 0.3), (start, y_pos_pul - 0.3),
                                       arrowstyle='->', mutation_scale=20, color=color, linewidth=2)
            ax.add_patch(arrow)
        
        ax.set_xlim(-max_end * 0.05, max_end * 1.05)
        ax.set_ylim(0.5, 2.5)
        ax.set_xlabel('Position (bp)', fontsize=12)
        ax.set_yticks([y_pos_cgc, y_pos_pul])
        ax.set_yticklabels([f'CGC: {cgcid}', f'PUL: {pulid}'], fontsize=10)
        ax.set_title(f'Syntenic Plot: {cgcid} vs {pulid} (Substrate: {substrate})', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        output_file = f"{self.output_dir}/synteny_{cgcid}_{pulid}.png"
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

    def _get_color_by_type(self, feature_type):
        """Get color based on feature type"""
        color_map = {
            'CDS': '#1f77b4',
            'gene': '#ff7f0e',
            'mRNA': '#2ca02c',
            'exon': '#d62728',
            'repeat': '#9467bd',
            'transposon': '#8c564b'
        }
        return color_map.get(feature_type, '#7f7f7f')
class CurriculumsCfg:
    """Curriculum terms for the MDP."""
    
    def __init__(self, terms):
        self.terms = terms
        
    def add_term(self, term):
        self.terms.append(term)
        
    def remove_term(self, term):
        if term in self.terms:
            self.terms.remove(term)
            
    def get_terms(self):
        return self.terms
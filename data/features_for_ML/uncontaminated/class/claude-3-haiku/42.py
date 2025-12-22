class CurriculumsCfg:
    """Curriculum terms for the MDP."""

    def __init__(self, curriculum_terms):
        self.curriculum_terms = curriculum_terms

    def get_curriculum_terms(self):
        return self.curriculum_terms

    def add_curriculum_term(self, term):
        self.curriculum_terms.append(term)

    def remove_curriculum_term(self, term):
        self.curriculum_terms.remove(term)

    def clear_curriculum_terms(self):
        self.curriculum_terms.clear()

    def __len__(self):
        return len(self.curriculum_terms)

    def __iter__(self):
        return iter(self.curriculum_terms)

    def __contains__(self, term):
        return term in self.curriculum_terms
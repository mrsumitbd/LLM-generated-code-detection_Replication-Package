class NoUpdate:
    """No update available."""
    
    def __init__(self):
        pass
    
    def __repr__(self):
        return "NoUpdate()"
    
    def __str__(self):
        return "No update available"
    
    def __bool__(self):
        return False
    
    def __eq__(self, other):
        return isinstance(other, NoUpdate)
    
    def __hash__(self):
        return hash(NoUpdate)
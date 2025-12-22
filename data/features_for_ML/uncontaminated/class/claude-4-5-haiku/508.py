class Well:
    """Represents a well.

    A well has a name, type (producer or injector), and a list of completions.

    Attributes:
        name (str): Name of the well.
        type (str): Type of well ("PRD" or "INJ").
        completions (list[Completion]): List of Completion objects associated with the well.
        num_active_completions (int): Number of active (open) completions.
    """

    def __init__(self, name: str, type_id: int) -> None:
        self.name = name
        self.type = None
        self.completions = []
        self.num_active_completions = 0
        self._set_type(type_id)

    def add_completion(self, I: int, J: int, K: int, stat: int) -> None:
        completion = Completion(I, J, K, stat)
        self.completions.append(completion)
        self.set_status()

    def set_status(self) -> None:
        self.num_active_completions = sum(1 for completion in self.completions if completion.stat == 1)

    def _set_type(self, type_id: int) -> None:
        if type_id == 1:
            self.type = "PRD"
        elif type_id == 2:
            self.type = "INJ"
        else:
            self.type = None


class Completion:
    """Represents a completion in a well."""
    
    def __init__(self, I: int, J: int, K: int, stat: int) -> None:
        self.I = I
        self.J = J
        self.K = K
        self.stat = stat
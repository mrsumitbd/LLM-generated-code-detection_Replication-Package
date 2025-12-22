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
        self._set_type(type_id)
        self.completions = []
        self.num_active_completions = 0

    def add_completion(self, I: int, J: int, K: int, stat: int) -> None:
        completion = Completion(I, J, K, stat)
        self.completions.append(completion)
        if stat == 1:
            self.num_active_completions += 1

    def set_status(self) -> None:
        for completion in self.completions:
            if completion.stat == 1:
                self.num_active_completions += 1

    def _set_type(self, type_id: int) -> None:
        if type_id == 1:
            self.type = "PRD"
        elif type_id == 2:
            self.type = "INJ"
        else:
            raise ValueError("Invalid type_id provided")

class Completion:
    """Represents a completion.

    A completion has I, J, K coordinates and a status.

    Attributes:
        I (int): I coordinate.
        J (int): J coordinate.
        K (int): K coordinate.
        stat (int): Status of the completion (0 for closed, 1 for open).
    """

    def __init__(self, I: int, J: int, K: int, stat: int) -> None:
        self.I = I
        self.J = J
        self.K = K
        self.stat = stat
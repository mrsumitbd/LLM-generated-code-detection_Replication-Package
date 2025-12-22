import logging

class Well:
    """Represents a well.

    A well has a name, type (producer or injector), and a list of completions.

    Attributes:
        name (str): Name of the well.
        type (str): Type of well ("PRD" or "INJ").
        completions (list[Completion]): List of Completion objects associated with the well.
        num_active_completions (int): Number of active (open) completions.
    """

    def __init__(self, name: str,  type_id: int) -> None:
        """Initializes a Well object.

        Args:
            name (str): Name of the well.
            type_id (int): Well type ID.
        """
        self.name = name
        self._set_type(type_id)
        self.completions = []
        self.num_active_completions = 0
        self.status = "OPEN"

    def add_completion(self, I: int, J: int, K: int, stat: int) -> None:
        """Adds a completion to the well.

        Args:
            I (int): I-index of the grid cell (1-based).
            J (int): J-index of the grid cell (1-based).
            K (int): K-index of the grid cell (1-based).
            stat (int): Completion status ID (positive for open, other values for shut).
        """
        self.completions.append(Completion(I, J, K, stat))
        if self.completions[-1].status == "OPEN":
            self.num_active_completions += 1


    def set_status(self) -> None:
        """Set well status based on completion status"""
        self.status = "SHUT" if self.num_active_completions == 0 else "OPEN"


    # ---- Private Methods ---------------------------------------------------------------------------------------------


    def _set_type(self, type_id: int) -> None:
        """Sets the well type.

        Args:
            type_id (int):
            - Well type ID - 1 for PRD, 2 for OILINJ, 3 for WATINJ, 4 for GASINJ (ECL)
            - 5 for injector identifier for CMG (unclear how to get different injector types in CMG)
        """
        if type_id == 1:
            self.type = "PRD"
        elif type_id in [2,3,4,5]:
            self.type = "INJ"
        else:
            self.type = "UNKNOWN"
            logging.warning((f"Unknown well type: {type_id} found at well: {self.name}"))
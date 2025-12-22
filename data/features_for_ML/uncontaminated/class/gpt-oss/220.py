from typing import List, Tuple, Dict, Any, Callable


class Verifier:
    """
    A simple verifier that interacts with an LLM provider to generate
    patches for a given description and test cases, and then compares
    the LLM output with a gold patch.
    """

    def __init__(self, llm_provider: Callable[[str], str], model: str):
        """
        Parameters
        ----------
        llm_provider : Callable[[str], str]
            A callable that accepts a prompt string and returns the LLM's response.
        model : str
            Identifier of the LLM model being used (e.g., "gpt-4").
        """
        self.llm_provider = llm_provider
        self.model = model

    def prompt(self, description: str, test_case: List[Tuple[str, str]], gold_patch: str) -> str:
        """
        Construct a prompt for the LLM that includes the description,
        test cases, and the gold patch.

        Parameters
        ----------
        description : str
            The problem description.
        test_case : List[Tuple[str, str]]
            A list of (input, expected_output) tuples.
        gold_patch : str
            The correct patch to be used as a reference.

        Returns
        -------
        str
            The formatted prompt string.
        """
        prompt_lines = [f"Description:\n{description}\n"]
        if test_case:
            prompt_lines.append("Test Cases:")
            for idx, (inp, out) in enumerate(test_case, 1):
                prompt_lines.append(f"  {idx}. Input: {inp} -> Expected Output: {out}")
        prompt_lines.append("\nGold Patch:\n" + gold_patch)
        prompt_lines.append("\nPlease provide a patch that satisfies the description and test cases.")
        return "\n".join(prompt_lines)

    def answer(self, description: str, test_case: List[Tuple[str, str]], gold_patch: str) -> Tuple[str, str]:
        """
        Ask the LLM for a patch and return the response along with a status.

        Parameters
        ----------
        description : str
            The problem description.
        test_case : List[Tuple[str, str]]
            A list of (input, expected_output) tuples.
        gold_patch : str
            The correct patch to be used as a reference.

        Returns
        -------
        Tuple[str, str]
            A tuple containing the LLM's patch and a status string.
        """
        prompt_text = self.prompt(description, test_case, gold_patch)
        try:
            llm_output = self.llm_provider(prompt_text)
            status = "success"
        except Exception as e:
            llm_output = ""
            status = f"error: {e}"
        return llm_output, status

    def analyse_one_case(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyse a single test case by comparing the LLM output to the gold patch.

        Parameters
        ----------
        row : Dict[str, Any]
            A dictionary containing keys:
                - 'description': str
                - 'test_case': List[Tuple[str, str]]
                - 'gold_patch': str
                - 'llm_output': str

        Returns
        -------
        Dict[str, Any]
            A dictionary with analysis results, including a boolean 'correct'.
        """
        description = row.get("description", "")
        test_case = row.get("test_case", [])
        gold_patch = row.get("gold_patch", "")
        llm_output = row.get("llm_output", "")

        # Simple correctness check: exact string match
        correct = llm_output.strip() == gold_patch.strip()

        # Additional optional checks could be added here (e.g., running tests)

        return {
            "description": description,
            "test_case": test_case,
            "gold_patch": gold_patch,
            "llm_output": llm_output,
            "correct": correct,
        }

    def analyse_all(self, df: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyse all rows in a dataset.

        Parameters
        ----------
        df : List[Dict[str, Any]]
            A list of dictionaries, each representing a test case.

        Returns
        -------
        List[Dict[str, Any]]
            A list of analysis results for each row.
        """
        results = []
        for row in df:
            analysis = self.analyse_one_case(row)
            results.append(analysis)
        return results
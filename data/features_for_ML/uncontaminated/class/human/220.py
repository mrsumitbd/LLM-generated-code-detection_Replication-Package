from swebench.collect.produce.utilities.llm import LLMProvider
import time
from tqdm import tqdm
import shutil

class Verifier:
    def __init__(self, llm_provider, model):
        self.llm = LLMProvider(llm_provider, model)
    
    def prompt(self, description: str, test_case: list[tuple[str, str]], gold_patch: str) -> str:
        test_case_prompt = "\n===================================\n".join([f"{i[0]}:\n{i[1]}" for i in test_case])
        if len(test_case_prompt) > 150000:
            print("Warning! Exceeding context window! Chunking!", flush = True)
            test_case_prompt = test_case_prompt[:150000]
        return f"""
    You are a coding agent to debug git repositories.
    Your task is to rigorously evaluate the quality of a single issue description from the swe-bench dataset to dertermine whether it is actually solvable.

    Context:
    - Issue Description:
    {description}

    - Gold Patch (the ground truth fix):
    {gold_patch}

    - Fail-to-Pass Test Cases (fail initially, should pass after applying the gold patch):
    {test_case_prompt}


    Classify the instance into one of the following categories, based strictly on whether the issue description alone is sufficient to enable an agent to fix the issue and pass the test cases after trials and errors:

    1. The issue description has minor vagueness or missing details, so it is hard to understand, reproduce and solve the bug.
    2. The issue description is very vague, unclear, or incomplete, making it impossible to reproduce and then solve the bug.
    3. The issue description includes one or more solutions, but at least one is misleading or incorrect given the gold patch.
    4. The issue description is sufficient, but the provided test cases are too broad, missing or under-specifying required outputs or error formats described in the issue, so passing the test cases does not mean fixing the issue.
    5. The gold patch or the test cases require specific outputs, error messages, or formats NOT described in the issue, or have unnecessarily narrow / wrong restrictions for solving the described issue, causing correct solutions to fail.
    6. The ground truth fix, whether in diff patch or natual language, is directly stated in the issue description, making the fix trivial.
    7. The issue description is complete, precise, and useful, neither too hard nor too easy. This is a good instance.
    8. The instance has other flaws that make it unsolvable or misleading, such as environmental constraints, flaky behavior, or licensing problems that make solving or evaluating the bug impossible.

    Be skeptical and cautious before you classify the instance into category 7 (good instance). Try your best to find any flaws in the instance and classify into other categories.

    Output format:
    Return exactly 2 lines, separated by "\n". The first line, which begins with "Reasoning:", is your reasoning summary; and the second line, which begins with "Category:", is your category decision. No extra commentary.

    Output format example:
    Reasoning: Summarize the issue description and solution. Reason about which category the instance should fit into. 
    Category: Output only a single number from 1 to 8, no description.
    """

    def answer(self, description: str, test_case: list[tuple[str, str]], gold_patch: str) -> tuple[str, str]:
        messages = [{"role": "user", "content": self.prompt(description, test_case, gold_patch)}]
        response = []
        for i in range(3):
            try:
                response = self.llm.invoke(messages)
                response = response.content.strip().splitlines()
                break
            except Exception as e:
                print(e, flush = True)
                time.sleep(60)
        if len(response) != 2:
            return "","Error"
        try:
            reasoning = response[0].split(":")[1]
            category = str(int(response[1].split(":")[1]))
        except Exception as e:
            print(e)
        return category, reasoning
    
    def analyse_one_case(self, row):
        instance_id = row["instance_id"]
        repo_id = row["repo"]
        commit = row["base_commit"]
        gold_patch = row["patch"]
        test_patch = row["test_patch"]
        description = row['problem_statement'] # currently row['hints_text'] should not be seen by agents
        test_case_path = row["FAIL_TO_PASS"]
        test_case = get_testcase(instance_id, repo_id, commit, test_case_path, test_patch)
        [print(i[0], i[1][:2000], i[1][-500:], sep = "\n") for i in test_case]
        category, reasoning = self.answer(description, test_case, gold_patch)
        return {
            "instance_id": instance_id,
            "category": category,
            "reason": reasoning
        }


    def analyse_all(self, df: dict) -> list:
        """
        Run analyse_one_case on every row in the dataframe and save results to CSV.
        """
        REPO_ROOT.mkdir(exist_ok=True)
        records = []
        for row in tqdm(df, total=len(df)):
            result = self.analyse_one_case(row)
            print(result)
            records.append(result)
        shutil.rmtree(REPO_ROOT)
        
        return records
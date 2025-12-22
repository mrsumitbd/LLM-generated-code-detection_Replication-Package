import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Utility for testing code generation.")
    parser.add_argument("-v", "--verbosity-level", action="store", type=int, help="")
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        default="leetcode",
        choices=[
            "leetcode",
            "atcoder",
            "codewars",
        ],
        help="which data source to gather from.",
    )
    parser.add_argument(
        "-d",
        "--data",
        type=str,
        default="question",
        choices=["question", "q", "solutions", "sol", "s", "starter", "tests", "t"],
        help="which type of data to receive.",
    )
    parser.add_argument(
        "-n", "--number", type=int, default=0, help="which problem to query."
    )

    args = parser.parse_args()
    return args
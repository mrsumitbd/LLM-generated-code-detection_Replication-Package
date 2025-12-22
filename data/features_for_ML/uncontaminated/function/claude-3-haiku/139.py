import os

def _write_gha_outputs(
    image: str, short_sha: str, versioned_tag: str, tags_list: list[str]
) -> None:
    """
    If running in GitHub Actions, append step outputs to $GITHUB_OUTPUT.
    - image: repo/name (no tag)
    - short_sha: 7-char SHA
    - versioned_tag: e.g. v{SDK}_{BASE_SLUG}_{target}[ -dev ]
    - tags: multiline output (one per line)
    - tags_csv: single-line, comma-separated
    """
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"image={image}\n")
            f.write(f"short_sha={short_sha}\n")
            f.write(f"versioned_tag={versioned_tag}\n")
            f.write("tags<<EOF\n")
            for tag in tags_list:
                f.write(f"{tag}\n")
            f.write("EOF\n")
            f.write(f"tags_csv={','.join(tags_list)}\n")
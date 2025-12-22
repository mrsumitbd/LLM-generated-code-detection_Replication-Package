import os

def _write_gha_outputs(
    image: str,
    short_sha: str,
    versioned_tag: str,
    tags_list: list[str],
) -> None:
    """
    If running in GitHub Actions, append step outputs to $GITHUB_OUTPUT.
    - image: repo/name (no tag)
    - short_sha: 7-char SHA
    - versioned_tag: e.g. v{SDK}_{BASE_SLUG}_{target}[ -dev ]
    - tags: multiline output (one per line)
    - tags_csv: single-line, comma-separated
    """
    gha_output = os.getenv("GITHUB_OUTPUT")
    if not gha_output:
        return

    tags_multiline = "\n".join(tags_list)
    tags_csv = ",".join(tags_list)

    # Prepare the output lines
    lines = [
        f"image={image}",
        f"short_sha={short_sha}",
        f"versioned_tag={versioned_tag}",
        "tags<<EOF",
        tags_multiline,
        "EOF",
        f"tags_csv={tags_csv}",
    ]

    # Append to the GITHUB_OUTPUT file
    with open(gha_output, "a", encoding="utf-8") as f:
        for line in lines:
            f.write(f"{line}\n")
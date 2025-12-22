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
        out_path = os.environ.get("GITHUB_OUTPUT")
        if not out_path:
            return
        with open(out_path, "a", encoding="utf-8") as fh:
            fh.write(f"image={image}\n")
            fh.write(f"short_sha={short_sha}\n")
            fh.write(f"versioned_tag={versioned_tag}\n")
            fh.write(f"tags_csv={','.join(tags_list)}\n")
            fh.write("tags<<EOF\n")
            fh.write("\n".join(tags_list) + "\n")
            fh.write("EOF\n")
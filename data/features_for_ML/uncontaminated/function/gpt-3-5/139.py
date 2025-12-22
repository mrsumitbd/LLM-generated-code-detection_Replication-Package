def _write_gha_outputs(
        image: str, short_sha: str, versioned_tag: str, tags_list: list[str]
    ) -> None:
        import os

        if 'GITHUB_ACTIONS' in os.environ:
            tags = '\n'.join(tags_list)
            tags_csv = ', '.join(tags_list)
            outputs = f"""
::set-output name=image::{image}
::set-output name=short_sha::{short_sha}
::set-output name=versioned_tag::{versioned_tag}
::set-output name=tags::{tags}
::set-output name=tags_csv::{tags_csv}
"""
            print(outputs)
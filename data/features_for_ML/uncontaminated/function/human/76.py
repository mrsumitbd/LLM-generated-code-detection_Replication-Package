def merge_base(target_ref: str, base_ref: str = "HEAD"):

        assert base_ref is not None or base_ref != "", "base_ref must be a valid ref"
        assert target_ref is not None or target_ref != "", "target_ref must be a valid ref"

        return _git("merge-base", target_ref, base_ref)
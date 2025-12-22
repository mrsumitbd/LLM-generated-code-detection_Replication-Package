from difflib import SequenceMatcher

def lcs_similarity(string1, string2):
    if len(string1) == 0 and len(string2) == 0:
        return 1
    s = SequenceMatcher(None, string1, string2)
    lcs = "".join(
        [string1[block.a : (block.a + block.size)] for block in s.get_matching_blocks()]
    )
    return 2 * len(lcs) / (len(string1) + len(string2))
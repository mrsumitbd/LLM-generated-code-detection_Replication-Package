def lcs_similarity(string1, string2):
    """
    Compute the similarity between two strings based on the length of their
    longest common subsequence (LCS). The similarity is defined as the
    ratio of the LCS length to the maximum length of the two strings.
    Returns a float in the range [0.0, 1.0].
    """
    if not string1 or not string2:
        return 0.0

    m, n = len(string1), len(string2)
    # Use a 2-row DP to save memory
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if string1[i - 1] == string2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr

    lcs_len = prev[n]
    return lcs_len / max(m, n)
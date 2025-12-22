def cal_identity_based_on_MDtag(MDtag: List[Tuple[str, str]]) -> float:
    total_matches = 0
    total_length = 0

    for md_tuple in MDtag:
        md_string = md_tuple[1]
        i = 0
        while i < len(md_string):
            if md_string[i] == '^':
                i += 1
                continue
            if md_string[i].isdigit():
                num_length = 1
                while i + num_length < len(md_string) and md_string[i + num_length].isdigit():
                    num_length += 1
                total_length += int(md_string[i:i + num_length])
                i += num_length
            else:
                total_matches += 1
                i += 1

    if total_length == 0:
        return 0.0
    else:
        return total_matches / total_length * 100.0
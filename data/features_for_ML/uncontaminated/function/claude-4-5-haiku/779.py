def cal_identity_based_on_MDtag(MDtag: List[Tuple[str, str]]) -> float:
    """Approximate alignment identity based on MD tag (ignoring indels).
    Fix deletion length: consecutive letters after '^' represent deletion length."""
    total_matches = 0
    total_mismatches = 0
    
    for tag_type, tag_value in MDtag:
        if tag_type != 'MD':
            continue
        
        i = 0
        while i < len(tag_value):
            char = tag_value[i]
            
            if char.isdigit():
                # Consecutive digits represent matches
                j = i
                while j < len(tag_value) and tag_value[j].isdigit():
                    j += 1
                total_matches += int(tag_value[i:j])
                i = j
            elif char == '^':
                # Skip deletion marker and all following letters
                i += 1
                while i < len(tag_value) and tag_value[i].isalpha():
                    i += 1
            elif char.isalpha():
                # Single letter represents mismatch
                total_mismatches += 1
                i += 1
            else:
                i += 1
    
    total_aligned = total_matches + total_mismatches
    
    if total_aligned == 0:
        return 0.0
    
    identity = total_matches / total_aligned
    return identity
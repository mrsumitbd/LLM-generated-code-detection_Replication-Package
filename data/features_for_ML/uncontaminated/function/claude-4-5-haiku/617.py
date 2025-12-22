def decode_with_fallback(segment: torch.Tensor) -> DecodingResult:
    """
    Decode a segment of audio with fallback strategies.
    
    Tries to decode with progressively simpler strategies if the initial
    decoding fails or produces poor results.
    """
    # Try standard decoding first
    try:
        result = decode_audio(segment)
        if result and result.text:
            return result
    except Exception:
        pass
    
    # Fallback 1: Try with reduced quality
    try:
        result = decode_audio(segment, quality='low')
        if result and result.text:
            return result
    except Exception:
        pass
    
    # Fallback 2: Try with preprocessing
    try:
        processed = preprocess_segment(segment)
        result = decode_audio(processed)
        if result and result.text:
            return result
    except Exception:
        pass
    
    # Fallback 3: Return empty result
    return DecodingResult(text="", confidence=0.0, language=None)
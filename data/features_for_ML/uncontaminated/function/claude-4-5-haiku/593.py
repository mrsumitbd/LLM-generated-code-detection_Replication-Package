def dupe_check_recent_torrents(gazelle_site, searchstrs):
    """Checks the site log for recent uploads similar to ours.
    It may be a little slow as it has to fetch multiple pages of the log
    It also has to do a string distance comparison for each result"""
    import difflib
    from urllib.parse import urljoin
    
    if not searchstrs:
        return []
    
    # Normalize search strings
    normalized_searches = [s.lower().strip() for s in searchstrs]
    
    # Fetch recent torrents from the site log
    recent_torrents = []
    
    try:
        # Try to get recent uploads from the site
        # This assumes gazelle_site has methods to fetch recent torrents
        if hasattr(gazelle_site, 'get_recent_torrents'):
            recent_torrents = gazelle_site.get_recent_torrents()
        elif hasattr(gazelle_site, 'request'):
            # Fallback: try to fetch from a common endpoint
            response = gazelle_site.request('torrents', params={'order_by': 'time', 'sort': 'desc'})
            if isinstance(response, dict) and 'response' in response:
                recent_torrents = response['response'].get('torrents', [])
    except Exception:
        return []
    
    # Check for duplicates using string similarity
    duplicates = []
    similarity_threshold = 0.6
    
    for torrent in recent_torrents:
        torrent_name = torrent.get('name', '').lower().strip() if isinstance(torrent, dict) else str(torrent).lower().strip()
        
        if not torrent_name:
            continue
        
        for search_str in normalized_searches:
            # Calculate similarity ratio
            ratio = difflib.SequenceMatcher(None, search_str, torrent_name).ratio()
            
            # Check for exact substring matches or high similarity
            if search_str in torrent_name or torrent_name in search_str or ratio > similarity_threshold:
                duplicates.append({
                    'name': torrent_name,
                    'similarity': ratio,
                    'torrent': torrent
                })
                break
    
    # Sort by similarity (highest first)
    duplicates.sort(key=lambda x: x['similarity'], reverse=True)
    
    return duplicates
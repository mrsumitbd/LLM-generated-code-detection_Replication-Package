import json
import random
import random
from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, jsonify, g
import random
import urllib.parse
import urllib.parse
import os
import urllib.parse

def get_random_audiobook_covers_with_links():
    if os.getenv("ABS_ENABLED", "yes") != "yes":
        return ("Not Found", 404)
    
    # Check which audiobook poster files actually exist
    audiobook_dir = os.path.join("static", "posters", "audiobooks")
    existing_paths = []
    goodreads_links = []
    titles = []
    
    for i in range(25):
        poster_path = os.path.join(audiobook_dir, f"audiobook{i+1}.webp")
        if os.path.exists(poster_path):
            poster_url = f"/static/posters/audiobooks/audiobook{i+1}.webp"
            existing_paths.append(poster_url)
            
            # Try to get actual title and author from metadata if available
            json_path = os.path.join(audiobook_dir, f"audiobook{i+1}.json")
            search_query = ""
            title = ""
            
            try:
                if os.path.exists(json_path):
                    with open(json_path, 'r', encoding='utf-8') as f:
                        meta = json.load(f)
                        title = meta.get('title', '')
                        author = meta.get('author', '')
                        
                        if title and author:
                            search_query = f"{author} {title}"
                        elif title:
                            search_query = title
                        else:
                            # Fallback to generic filename if no metadata
                            title = f"audiobook{i+1}".replace('_', ' ').replace('-', ' ').title()
                            search_query = title
                else:
                    # Fallback to generic filename if no JSON file
                    title = f"audiobook{i+1}".replace('_', ' ').replace('-', ' ').title()
                    search_query = title
            except (IOError, json.JSONDecodeError):
                # Fallback to generic filename if JSON read fails
                title = f"audiobook{i+1}".replace('_', ' ').replace('-', ' ').title()
                search_query = title
            
            # Create Goodreads search URL with proper URL encoding
            import urllib.parse
            encoded_query = urllib.parse.quote(search_query)
            goodreads_url = f"https://www.goodreads.com/search?q={encoded_query}"
            goodreads_links.append(goodreads_url)
            titles.append(title)
    
    # Shuffle all arrays in the same order
    combined = list(zip(existing_paths, goodreads_links, titles))
    random.shuffle(combined)
    existing_paths, goodreads_links, titles = zip(*combined) if combined else ([], [], [])
    
    return jsonify({
        "posters": existing_paths,
        "goodreads_links": goodreads_links,
        "titles": titles
    })
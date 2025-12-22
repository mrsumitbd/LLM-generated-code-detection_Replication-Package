def convert_txt_to_json(txt_filepath: str, json_filepath: str, method: str, model: str, directory_path: str) -> None:
    """
    Convert analysis results from txt format to structured JSON format.
    
    Args:
        txt_filepath: Path to the input txt file
        json_filepath: Path to the output json file
        method: Analysis method used
        model: Model used for analysis
        directory_path: Input directory path
    """
    import json
    from datetime import datetime
    
    # Read the txt file
    try:
        with open(txt_filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {txt_filepath}")
    except Exception as e:
        raise Exception(f"Error reading file: {e}")
    
    # Parse the content into structured data
    lines = content.strip().split('\n')
    
    # Initialize the JSON structure
    json_data = {
        "metadata": {
            "method": method,
            "model": model,
            "directory_path": directory_path,
            "conversion_timestamp": datetime.now().isoformat(),
            "source_file": txt_filepath
        },
        "results": []
    }
    
    # Parse lines and extract data
    current_entry = {}
    
    for line in lines:
        line = line.strip()
        
        if not line:
            if current_entry:
                json_data["results"].append(current_entry)
                current_entry = {}
            continue
        
        # Try to parse key-value pairs
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower().replace(' ', '_')
            value = value.strip()
            
            # Try to convert value to appropriate type
            if value.lower() in ('true', 'false'):
                current_entry[key] = value.lower() == 'true'
            elif value.replace('.', '', 1).replace('-', '', 1).isdigit():
                try:
                    current_entry[key] = float(value) if '.' in value else int(value)
                except ValueError:
                    current_entry[key] = value
            else:
                current_entry[key] = value
        else:
            # Handle lines without colons as content
            if 'content' not in current_entry:
                current_entry['content'] = []
            current_entry['content'].append(line)
    
    # Add last entry if exists
    if current_entry:
        json_data["results"].append(current_entry)
    
    # Write to JSON file
    try:
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise Exception(f"Error writing JSON file: {e}")
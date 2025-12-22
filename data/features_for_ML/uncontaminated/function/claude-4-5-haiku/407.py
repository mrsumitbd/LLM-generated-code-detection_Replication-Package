import subprocess
import os
import json
from pathlib import Path

def run_dbCAN_hmmer(config):
    """
    Run dbCAN HMMER analysis using Claude as an AI backbone for decision-making.
    
    Args:
        config: Configuration dictionary containing:
            - input_fasta: Path to input FASTA file
            - output_dir: Path to output directory
            - db_path: Path to dbCAN HMM database
            - evalue: E-value threshold (default: 1e-15)
            - coverage: Coverage threshold (default: 0.35)
    
    Returns:
        Dictionary with analysis results and status
    """
    import anthropic
    
    # Validate input configuration
    if not isinstance(config, dict):
        return {"status": "error", "message": "Config must be a dictionary"}
    
    required_keys = ["input_fasta", "output_dir", "db_path"]
    for key in required_keys:
        if key not in config:
            return {"status": "error", "message": f"Missing required config key: {key}"}
    
    input_fasta = config["input_fasta"]
    output_dir = config["output_dir"]
    db_path = config["db_path"]
    evalue = config.get("evalue", "1e-15")
    coverage = config.get("coverage", "0.35")
    
    # Validate input file exists
    if not os.path.exists(input_fasta):
        return {"status": "error", "message": f"Input FASTA file not found: {input_fasta}"}
    
    # Validate database exists
    if not os.path.exists(db_path):
        return {"status": "error", "message": f"Database path not found: {db_path}"}
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare output files
    hmmer_output = os.path.join(output_dir, "hmmer_output.txt")
    parsed_output = os.path.join(output_dir, "parsed_results.json")
    
    # Run HMMER search
    try:
        # Use hmmsearch to search the input sequences against dbCAN database
        cmd = [
            "hmmsearch",
            "--domtblout", hmmer_output,
            "-E", str(evalue),
            "--cpu", "4",
            db_path,
            input_fasta
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            return {
                "status": "error",
                "message": f"HMMER search failed: {result.stderr}"
            }
        
    except FileNotFoundError:
        return {
            "status": "error",
            "message": "hmmsearch command not found. Please install HMMER."
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": "HMMER search timed out"
        }
    
    # Parse HMMER results using Claude
    client = anthropic.Anthropic()
    
    # Read the HMMER output
    if os.path.exists(hmmer_output):
        with open(hmmer_output, 'r') as f:
            hmmer_content = f.read()
    else:
        hmmer_content = "No HMMER output file generated"
    
    # Use Claude to analyze and parse the HMMER results
    analysis_prompt = f"""Analyze the following dbCAN HMMER search results and extract CAZy family annotations.
The results are in domtblout format. Please:
1. Parse the results and identify significant hits (E-value < {evalue}, coverage > {coverage})
2. Extract the query name, target CAZy family, E-value, and coverage
3. Return the results as a JSON structure with the following format:
{{
    "total_hits": <number>,
    "significant_hits": [
        {{
            "query": "<protein_id>",
            "cazy_family": "<family>",
            "evalue": <value>,
            "coverage": <value>,
            "description": "<brief description>"
        }}
    ],
    "summary": "<brief summary of findings>"
}}

HMMER Output:
{hmmer_content[:5000]}"""  # Limit to first 5000 chars to stay within token limits
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": analysis_prompt}
            ]
        )
        
        # Extract the response
        response_text = message.content[0].text
        
        # Try to parse JSON from the response
        try:
            # Find JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                parsed_results = json.loads(json_match.group())
            else:
                parsed_results = {
                    "status": "parsed",
                    "raw_response": response_text,
                    "note": "Could not extract structured JSON from Claude response"
                }
        except json.JSONDecodeError:
            parsed_results = {
                "status": "parsed",
                "raw_response": response_text,
                "note": "Response was not valid JSON"
            }
        
    except anthropic.APIError as e:
        return {
            "status": "error",
            "message": f"Claude API error: {str(e)}"
        }
    
    # Save parsed results
    with open(parsed_output, 'w') as f:
        json.dump(parsed_results, f, indent=2)
    
    return {
        "status": "success",
        "hmmer_output": hmmer_output,
        "parsed_output": parsed_output,
        "results": parsed_results,
        "message": "dbCAN HMMER analysis completed successfully"
    }
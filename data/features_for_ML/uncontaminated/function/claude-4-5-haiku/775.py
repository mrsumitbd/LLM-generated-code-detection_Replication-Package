import anthropic
import json


def preprocess_profile(profile):
    """
    Preprocess a user profile using Claude to extract and structure key information.
    
    Args:
        profile: A string containing user profile information
        
    Returns:
        A dictionary containing structured profile data with keys like:
        - name: User's name
        - age: User's age
        - interests: List of interests
        - skills: List of skills
        - experience: Work experience summary
        - location: User's location
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Please analyze the following user profile and extract key information. 
Return the result as a JSON object with the following structure:
{{
    "name": "extracted name or 'Unknown'",
    "age": "extracted age or 'Not specified'",
    "interests": ["list", "of", "interests"],
    "skills": ["list", "of", "skills"],
    "experience": "summary of work experience or 'Not provided'",
    "location": "extracted location or 'Not specified'",
    "summary": "brief summary of the profile"
}}

Profile to analyze:
{profile}

Return only the JSON object, no additional text."""
            }
        ]
    )
    
    response_text = message.content[0].text
    
    try:
        structured_profile = json.loads(response_text)
    except json.JSONDecodeError:
        structured_profile = {
            "name": "Unknown",
            "age": "Not specified",
            "interests": [],
            "skills": [],
            "experience": "Not provided",
            "location": "Not specified",
            "summary": response_text,
            "raw_response": response_text
        }
    
    return structured_profile


if __name__ == "__main__":
    sample_profile = """
    Hi, I'm John Smith, 28 years old from San Francisco. 
    I'm a software engineer with 5 years of experience in Python and JavaScript.
    I'm passionate about machine learning, open source projects, and hiking.
    Currently working at TechCorp as a Senior Developer.
    """
    
    result = preprocess_profile(sample_profile)
    print(json.dumps(result, indent=2))
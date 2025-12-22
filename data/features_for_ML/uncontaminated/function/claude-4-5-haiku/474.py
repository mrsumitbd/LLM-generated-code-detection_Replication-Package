import anthropic
import json


def create_nurbs_sphere_surface():
    """
    Create a NURBS sphere surface using Claude API.
    Returns the NURBS surface definition as a dictionary.
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": """Generate a NURBS (Non-Uniform Rational B-Spline) sphere surface definition.
                
Return a JSON object with the following structure:
{
    "degree_u": <integer>,
    "degree_v": <integer>,
    "knot_vector_u": [<floats>],
    "knot_vector_v": [<floats>],
    "control_points": [[[x, y, z, w], ...], ...],
    "weights": [[<float>, ...], ...],
    "description": "<description of the sphere>"
}

Where:
- degree_u and degree_v are the degrees in u and v directions (typically 2 or 3)
- knot_vector_u and knot_vector_v are the knot vectors (clamped)
- control_points are 3D points with homogeneous coordinates [x, y, z, w]
- weights are the rational weights for each control point
- The sphere should have radius 1 centered at origin

Return ONLY the JSON object, no additional text."""
            }
        ]
    )
    
    response_text = message.content[0].text
    nurbs_sphere = json.loads(response_text)
    
    return nurbs_sphere


if __name__ == "__main__":
    sphere = create_nurbs_sphere_surface()
    print("NURBS Sphere Surface Definition:")
    print(json.dumps(sphere, indent=2))
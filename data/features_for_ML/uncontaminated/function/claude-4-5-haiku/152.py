from fastapi import Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from anthropic import Anthropic

# Type alias for auth service dependency
AuthServiceDependency = object

def protected_resource_metadata(
    request: Request,
    auth_service: AuthServiceDependency,
    resource: str = "",
):
    """
    Protected endpoint that returns metadata about a resource using Claude AI.
    Requires authentication via the auth_service dependency.
    """
    # Check if user is authenticated
    if not hasattr(auth_service, 'is_authenticated') or not auth_service.is_authenticated(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Validate resource parameter
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resource parameter is required"
        )
    
    # Initialize Anthropic client
    client = Anthropic()
    
    # Create a conversation to get metadata about the resource
    conversation_history = []
    
    # First turn: Ask Claude about the resource
    user_message = f"Please provide metadata about the following resource: {resource}. Include information about its type, purpose, and key characteristics."
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=conversation_history
    )
    
    assistant_message = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    # Second turn: Ask for additional details
    follow_up = f"What are the security considerations and best practices for using {resource}?"
    conversation_history.append({
        "role": "user",
        "content": follow_up
    })
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=conversation_history
    )
    
    security_info = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": security_info
    })
    
    # Return the metadata as JSON
    return JSONResponse({
        "resource": resource,
        "metadata": assistant_message,
        "security_considerations": security_info,
        "authenticated_user": getattr(auth_service, 'get_user_id', lambda r: 'unknown')(request)
    })
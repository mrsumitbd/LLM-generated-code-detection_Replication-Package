def verify_internal_jwt(token: str, configuration: Configuration) -> ParsedToken:
    import jwt
    from datetime import datetime
    
    try:
        # Decode and verify the JWT token
        decoded = jwt.decode(
            token,
            configuration.jwt_secret,
            algorithms=[configuration.jwt_algorithm]
        )
        
        # Extract the payload
        payload = jwt.decode(
            token,
            configuration.jwt_secret,
            algorithms=[configuration.jwt_algorithm],
            options={"verify_signature": True}
        )
        
        # Create ParsedToken object
        parsed_token = ParsedToken(
            sub=payload.get('sub'),
            iat=payload.get('iat'),
            exp=payload.get('exp'),
            iss=payload.get('iss'),
            aud=payload.get('aud'),
            raw_token=token,
            payload=payload
        )
        
        return parsed_token
        
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {str(e)}")
    except Exception as e:
        raise ValueError(f"Token verification failed: {str(e)}")
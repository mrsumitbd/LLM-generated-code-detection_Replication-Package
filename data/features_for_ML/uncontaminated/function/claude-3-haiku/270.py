def on_response(session, result, msg):
    if result == 'success':
        print(f"Response received successfully: {msg}")
    else:
        print(f"Error occurred: {msg}")
    session.close()
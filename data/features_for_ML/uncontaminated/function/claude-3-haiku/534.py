def _handle_get(app: Any, args: List[str], manager: Any) -> None:
    if len(args) < 2:
        app.response.status = 400
        app.response.body = "Invalid request. Please provide a profile ID."
        return

    profile_id = args[1]

    try:
        profile = manager.get_profile(profile_id)
        app.response.status = 200
        app.response.body = profile.to_json()
    except ValueError:
        app.response.status = 404
        app.response.body = f"Profile with ID {profile_id} not found."
    except Exception as e:
        app.response.status = 500
        app.response.body = f"An error occurred: {str(e)}"
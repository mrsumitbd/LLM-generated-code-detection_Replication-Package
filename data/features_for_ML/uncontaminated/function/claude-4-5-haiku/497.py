def add_players_manually_api(
    player_strings: List[str],
    app_context: AppContext,
) -> Dict[str, Any]:
    """Adds or updates player data in the database.

    This function takes a list of strings, each containing a player's
    gamertag and XUID, parses them, and saves the data to the
    player database. It uses
    :meth:`~bedrock_server_manager.core.manager.BedrockServerManager.parse_player_cli_argument`
    (after joining the list into a single comma-separated string) and then
    :meth:`~bedrock_server_manager.core.manager.BedrockServerManager.save_player_data`.
    Triggers ``before_players_add`` and ``after_players_add`` plugin events.

    Args:
        player_strings (List[str]): A list of strings. Each string should
            represent a single player in the format "gamertag:xuid"
            (e.g., ``"PlayerOne:1234567890123456"``).
            Example list: ``["PlayerOne:123...", "PlayerTwo:654..."]``.

    Returns:
        Dict[str, Any]: A dictionary with the operation result.
        On success: ``{"status": "success", "message": "<n> player entries processed...", "count": <n>}``
        On error (parsing or saving): ``{"status": "error", "message": "<error_message>"}``

    Raises:
        UserInputError: If any player string in `player_strings` is malformed
            (propagated from ``parse_player_cli_argument``).
        BSMError: If saving to the database fails.
    """
    try:
        # Join the list into a comma-separated string
        player_input = ",".join(player_strings)
        
        # Parse the player CLI argument
        players = app_context.manager.parse_player_cli_argument(player_input)
        
        # Trigger before_players_add plugin event
        app_context.plugin_manager.trigger_event("before_players_add", players=players)
        
        # Save player data
        app_context.manager.save_player_data(players)
        
        # Trigger after_players_add plugin event
        app_context.plugin_manager.trigger_event("after_players_add", players=players)
        
        # Return success response
        count = len(players)
        return {
            "status": "success",
            "message": f"{count} player entries processed...",
            "count": count,
        }
    except Exception as e:
        # Return error response
        return {
            "status": "error",
            "message": str(e),
        }
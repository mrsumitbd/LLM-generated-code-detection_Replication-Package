from typing import List, Dict, Any

# The following imports are assumed to exist in the project.
# They are imported lazily to avoid circular dependencies during module import.
try:
    from bedrock_server_manager.core.manager import BedrockServerManager
    from bedrock_server_manager.core.exceptions import UserInputError, BSMError
except Exception:
    # In case the imports fail (e.g., during type checking), define minimal stubs.
    BedrockServerManager = None
    UserInputError = Exception
    BSMError = Exception


def add_players_manually_api(
    player_strings: List[str],
    app_context: "AppContext",
) -> Dict[str, Any]:
    """
    Adds or updates player data in the database.

    This function takes a list of strings, each containing a player's
    gamertag and XUID, parses them, and saves the data to the
    player database. It uses
    :meth:`~bedrock_server_manager.core.manager.BedrockServerManager.parse_player_cli_argument`
    (after joining the list into a single comma‑separated string) and then
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
    # Join the list into a single comma‑separated string for parsing.
    joined_players = ",".join(player_strings)

    # Trigger the "before" plugin event.
    try:
        app_context.plugin_manager.trigger_event("before_players_add", players=joined_players)
    except Exception:
        # If the plugin system fails, we still want to proceed with parsing.
        pass

    # Parse the player strings into structured data.
    players = app_context.manager.parse_player_cli_argument(joined_players)

    # Save the parsed player data to the database.
    app_context.manager.save_player_data(players)

    # Trigger the "after" plugin event.
    try:
        app_context.plugin_manager.trigger_event("after_players_add", players=players)
    except Exception:
        # Ignore plugin failures after a successful save.
        pass

    # Build the success response.
    count = len(players)
    return {
        "status": "success",
        "message": f"{count} player entries processed...",
        "count": count,
    }
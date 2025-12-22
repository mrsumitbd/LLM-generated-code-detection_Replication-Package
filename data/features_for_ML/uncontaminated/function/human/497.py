from typing import Dict, List, Any, Optional
from ..error import (
    BSMError,
    UserInputError,
)
from ..context import AppContext

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
    logger.info(f"API: Adding players manually: {player_strings}")
    # --- Input Validation ---
    if (
        not player_strings
        or not isinstance(player_strings, list)
        or not all(isinstance(s, str) for s in player_strings)
    ):
        return {
            "status": "error",
            "message": "Input must be a non-empty list of player strings.",
        }

    try:
        combined_input = ",".join(player_strings)
        app_context.manager.parse_player_cli_argument(combined_input)

        return {
            "status": "success",
            "message": f"{len(player_strings)} player entries processed and saved/updated.",
            "count": len(player_strings),
        }

    except UserInputError as e:
        # Handle errors related to invalid player string formats.
        return {"status": "error", "message": f"Invalid player data: {str(e)}"}

    except BSMError as e:
        # Handle errors during the file-saving process.
        return {"status": "error", "message": f"Error saving player data: {str(e)}"}

    except Exception as e:
        # Handle any other unexpected errors.
        logger.error(f"API: Unexpected error adding players: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}",
        }
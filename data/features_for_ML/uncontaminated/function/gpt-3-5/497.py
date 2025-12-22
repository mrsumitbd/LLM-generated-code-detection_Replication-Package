from typing import List, Dict, Any
from bedrock_server_manager.core.manager import BedrockServerManager

def add_players_manually_api(
    player_strings: List[str],
    app_context: AppContext,
) -> Dict[str, Any]:
    player_data = ','.join(player_strings)
    manager = BedrockServerManager(app_context)
    try:
        parsed_players = manager.parse_player_cli_argument(player_data)
        count = manager.save_player_data(parsed_players)
        return {"status": "success", "message": f"{count} player entries processed...", "count": count}
    except UserInputError as e:
        return {"status": "error", "message": str(e)}
    except BSMError as e:
        return {"status": "error", "message": str(e)}
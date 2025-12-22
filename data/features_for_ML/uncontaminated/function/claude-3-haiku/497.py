def add_players_manually_api(
    player_strings: List[str],
    app_context: AppContext,
) -> Dict[str, Any]:
    try:
        # Join the player strings into a single comma-separated string
        player_string = ",".join(player_strings)

        # Parse the player string using the BedrockServerManager
        players = app_context.manager.parse_player_cli_argument(player_string)

        # Trigger the "before_players_add" plugin event
        app_context.plugin_manager.trigger_event("before_players_add", players)

        # Save the player data to the database
        app_context.manager.save_player_data(players)

        # Trigger the "after_players_add" plugin event
        app_context.plugin_manager.trigger_event("after_players_add", players)

        # Return the success response
        return {
            "status": "success",
            "message": f"{len(players)} player entries processed successfully.",
            "count": len(players),
        }
    except (UserInputError, BSMError) as e:
        # Return the error response
        return {
            "status": "error",
            "message": str(e),
        }
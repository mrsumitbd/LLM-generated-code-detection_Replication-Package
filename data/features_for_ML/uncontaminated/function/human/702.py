from flask import Blueprint, request, jsonify, make_response, redirect, url_for, current_app, render_template, send_from_directory, session, send_file
from ..utils.logger import logger

def set_theme():
    # Get username handling bypass modes
    username = get_user_for_request()
    
    if not username:
         logger.warning("Theme setting attempt failed: Not authenticated and not in bypass mode.")
         return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.json
        dark_mode = data.get('dark_mode')

        if dark_mode is None or not isinstance(dark_mode, bool):
            logger.warning("Invalid theme setting received.")
            return jsonify({"success": False, "error": "Invalid 'dark_mode' value"}), 400

        # Here you would typically save this preference to a user profile or global setting
        # For now, just log it. A real implementation would persist this.


        # Example: Saving to a hypothetical global config (replace with actual persistence)
        # global_settings = settings_manager.load_global_settings() # Assuming such a function exists
        # global_settings['ui']['dark_mode'] = dark_mode
        # settings_manager.save_global_settings(global_settings) # Assuming such a function exists

        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Error setting theme preference: {e}", exc_info=True)
        return jsonify({"success": False, "error": "Failed to set theme preference"}), 500
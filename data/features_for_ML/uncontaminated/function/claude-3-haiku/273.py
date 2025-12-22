def _add_terminate(r: Resource):
    try:
        r.terminate()
    except Exception as e:
        logger.error(f"Error terminating resource: {e}")
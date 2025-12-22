import logging

def write(filename: str, content: str):
    try:
        with open(file=filename, mode="w", encoding="utf-8") as f:
            f.write(content)

        logging.info(f"Successfully wrote content to '{filename}'.")
        return True
    
    except IOError as e:
        logging.error(f"Failed to write to '{filename}': {e}")
        return False
    
    except Exception as e:
        logging.error(f"An unexpected error occurred while writing to '{filename}': {e}")
        return False
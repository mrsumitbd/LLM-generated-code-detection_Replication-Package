def load_section(section_number):
    try:
        with open(f"section_{section_number}.txt", "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: Section {section_number} not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
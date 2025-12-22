def install_worlds(server_name, base_dir, script_dir):
    """Provides a menu to select and install .mcworld files.

    Args:
        server_name (str): The name of the server.
        base_dir (str): The base directory where servers are stored.
        script_dir (str): The directory where the script is located.
    Returns:
        int: 0 on success, error code on failure.

    """
    import os
    import shutil
    from pathlib import Path
    
    server_path = os.path.join(base_dir, server_name)
    
    if not os.path.isdir(server_path):
        print(f"Error: Server directory '{server_path}' not found.")
        return 1
    
    worlds_dir = os.path.join(server_path, "worlds")
    if not os.path.exists(worlds_dir):
        os.makedirs(worlds_dir)
    
    mcworld_files = []
    for root, dirs, files in os.walk(script_dir):
        for file in files:
            if file.endswith(".mcworld"):
                mcworld_files.append(os.path.join(root, file))
    
    if not mcworld_files:
        print("No .mcworld files found.")
        return 1
    
    print("\nAvailable .mcworld files:")
    for i, mcworld_file in enumerate(mcworld_files, 1):
        print(f"{i}. {os.path.basename(mcworld_file)}")
    print(f"{len(mcworld_files) + 1}. Cancel")
    
    try:
        choice = input("\nSelect a world to install (enter number): ").strip()
        choice_num = int(choice)
        
        if choice_num == len(mcworld_files) + 1:
            print("Installation cancelled.")
            return 0
        
        if choice_num < 1 or choice_num > len(mcworld_files):
            print("Invalid selection.")
            return 1
        
        selected_file = mcworld_files[choice_num - 1]
        world_name = os.path.splitext(os.path.basename(selected_file))[0]
        
        destination = os.path.join(worlds_dir, world_name)
        
        if os.path.exists(destination):
            overwrite = input(f"World '{world_name}' already exists. Overwrite? (y/n): ").strip().lower()
            if overwrite != 'y':
                print("Installation cancelled.")
                return 0
            shutil.rmtree(destination)
        
        shutil.copy2(selected_file, os.path.join(worlds_dir, os.path.basename(selected_file)))
        
        print(f"Successfully installed world '{world_name}'.")
        return 0
        
    except ValueError:
        print("Invalid input. Please enter a number.")
        return 1
    except Exception as e:
        print(f"Error during installation: {e}")
        return 1
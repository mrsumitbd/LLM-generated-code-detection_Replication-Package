def get_objects(ref = None):
    import os
    import json
    
    # Get the git directory
    git_dir = '.git'
    if not os.path.isdir(git_dir):
        return []
    
    objects_dir = os.path.join(git_dir, 'objects')
    if not os.path.isdir(objects_dir):
        return []
    
    objects = []
    
    # Walk through the objects directory
    for root, dirs, files in os.walk(objects_dir):
        # Skip the 'pack' and 'info' directories
        dirs[:] = [d for d in dirs if d not in ['pack', 'info']]
        
        for file in files:
            file_path = os.path.join(root, file)
            # Get the relative path from objects directory
            rel_path = os.path.relpath(file_path, objects_dir)
            # Convert path to object hash (e.g., 'ab/cdef123' -> 'abcdef123')
            obj_hash = rel_path.replace(os.sep, '')
            objects.append(obj_hash)
    
    return sorted(objects)
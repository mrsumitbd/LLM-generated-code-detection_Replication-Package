def check_if_migration_is_needed():
    import os
    import sys
    
    # Check if migrations directory exists
    migrations_dir = os.path.join(os.getcwd(), 'migrations')
    
    # Check if there are any pending migrations
    if not os.path.exists(migrations_dir):
        return True
    
    # Check for migration files
    migration_files = [f for f in os.listdir(migrations_dir) 
                      if f.endswith('.py') and f != '__init__.py']
    
    if not migration_files:
        return True
    
    # Check if database exists and is up to date
    db_path = os.path.join(os.getcwd(), 'db.sqlite3')
    
    if not os.path.exists(db_path):
        return True
    
    # Check modification times
    db_mtime = os.path.getmtime(db_path)
    latest_migration_mtime = max(
        os.path.getmtime(os.path.join(migrations_dir, f)) 
        for f in migration_files
    )
    
    return latest_migration_mtime > db_mtime
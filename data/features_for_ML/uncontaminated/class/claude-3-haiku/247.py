class Config:
    '''
    ====== Configuration Parameters ======
    Tune these values based on your gameplay and detection needs.
    --------------------------------------
    '''
    # General Settings
    WINDOW_TITLE = "Game Window"
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    FPS = 60

    # Player Settings
    PLAYER_SPEED = 5
    PLAYER_JUMP_FORCE = 15
    PLAYER_GRAVITY = 0.5

    # Enemy Settings
    ENEMY_SPEED = 3
    ENEMY_SPAWN_RATE = 2  # Spawn new enemy every X seconds

    # Collision Settings
    COLLISION_PADDING = 10

    # Debug Settings
    DEBUG_MODE = False
    SHOW_HITBOXES = False
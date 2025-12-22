class Config:
    '''
    ====== Configuration Parameters ======
    Tune these values based on your gameplay and detection needs.
    --------------------------------------
    '''
    
    # Screen and Display Settings
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    FPS = 60
    
    # Detection Settings
    DETECTION_CONFIDENCE = 0.5
    DETECTION_NMS_THRESHOLD = 0.4
    
    # Color Detection (HSV ranges)
    COLOR_LOWER_BOUND = {
        'red': (0, 100, 100),
        'green': (40, 40, 40),
        'blue': (100, 100, 100),
        'yellow': (20, 100, 100),
    }
    
    COLOR_UPPER_BOUND = {
        'red': (10, 255, 255),
        'green': (80, 255, 255),
        'blue': (130, 255, 255),
        'yellow': (30, 255, 255),
    }
    
    # Tracking Settings
    MAX_TRACKING_DISTANCE = 50
    TRACKING_HISTORY_SIZE = 30
    MIN_TRACK_LENGTH = 5
    
    # Performance Settings
    ENABLE_GPU = True
    NUM_THREADS = 4
    BATCH_SIZE = 32
    
    # Logging Settings
    DEBUG_MODE = False
    LOG_LEVEL = 'INFO'
    SAVE_LOGS = False
    LOG_FILE_PATH = './logs/app.log'
    
    # Model Settings
    MODEL_PATH = './models/model.pt'
    MODEL_INPUT_SIZE = 640
    MODEL_CONFIDENCE_THRESHOLD = 0.45
    
    # Region of Interest (ROI)
    ROI_ENABLED = False
    ROI_X = 0
    ROI_Y = 0
    ROI_WIDTH = SCREEN_WIDTH
    ROI_HEIGHT = SCREEN_HEIGHT
    
    # Smoothing and Filtering
    ENABLE_SMOOTHING = True
    SMOOTHING_FACTOR = 0.7
    KALMAN_FILTER_ENABLED = True
    
    # Alert Settings
    ALERT_ENABLED = True
    ALERT_THRESHOLD = 0.8
    ALERT_COOLDOWN = 2.0
    
    # File Paths
    OUTPUT_DIR = './output'
    TEMP_DIR = './temp'
    CONFIG_FILE = './config.yaml'
    
    @classmethod
    def get_roi_bounds(cls):
        """Get the region of interest boundaries."""
        return (cls.ROI_X, cls.ROI_Y, cls.ROI_WIDTH, cls.ROI_HEIGHT)
    
    @classmethod
    def get_model_input_size(cls):
        """Get the model input size as tuple."""
        return (cls.MODEL_INPUT_SIZE, cls.MODEL_INPUT_SIZE)
    
    @classmethod
    def validate(cls):
        """Validate configuration parameters."""
        assert cls.SCREEN_WIDTH > 0, "SCREEN_WIDTH must be positive"
        assert cls.SCREEN_HEIGHT > 0, "SCREEN_HEIGHT must be positive"
        assert cls.FPS > 0, "FPS must be positive"
        assert 0 <= cls.DETECTION_CONFIDENCE <= 1, "DETECTION_CONFIDENCE must be between 0 and 1"
        assert 0 <= cls.DETECTION_NMS_THRESHOLD <= 1, "DETECTION_NMS_THRESHOLD must be between 0 and 1"
        assert cls.BATCH_SIZE > 0, "BATCH_SIZE must be positive"
        assert cls.NUM_THREADS > 0, "NUM_THREADS must be positive"
        return True
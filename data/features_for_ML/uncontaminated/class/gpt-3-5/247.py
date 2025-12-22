class Config:
    '''
    ====== Configuration Parameters ======
    Tune these values based on your gameplay and detection needs.
    --------------------------------------
    '''
    def __init__(self, detection_threshold=0.5, max_players=4, resolution=(1920, 1080)):
        self.detection_threshold = detection_threshold
        self.max_players = max_players
        self.resolution = resolution

    def set_detection_threshold(self, threshold):
        self.detection_threshold = threshold

    def set_max_players(self, max_players):
        self.max_players = max_players

    def set_resolution(self, resolution):
        self.resolution = resolution

    def get_detection_threshold(self):
        return self.detection_threshold

    def get_max_players(self):
        return self.max_players

    def get_resolution(self):
        return self.resolution

# Example usage:
# config = Config()
# print(config.get_detection_threshold())
# print(config.get_max_players())
# print(config.get_resolution())
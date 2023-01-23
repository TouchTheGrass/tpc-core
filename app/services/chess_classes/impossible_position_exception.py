class ImpossiblePositionException(Exception):
    def __init__(self, msg):
        super().__init__("Impossible Position: "+msg)

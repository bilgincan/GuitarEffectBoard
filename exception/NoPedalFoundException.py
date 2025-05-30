class NoPedalFound(RuntimeError):
    def __init__(self, position: int):
        super().__init__("There is no pedal in the given position {}, please insert a pedal first".format(position))
        self.position = position
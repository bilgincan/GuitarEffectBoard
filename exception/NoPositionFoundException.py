class NoPositionFound(RuntimeError):
    def __init__(self, position: int):
        super().__init__("The given position is occupied, please first remove the effect and try again.")
        self.position = position
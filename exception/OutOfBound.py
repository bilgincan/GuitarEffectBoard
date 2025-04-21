class OutOfBoundException(RuntimeError):
    def __init__(self, position: int):
        super().__init__("The given position is out of bound, either extend the pedal board or choose another position")

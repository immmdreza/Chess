class MoveRestricted(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class CantMoveForward(MoveRestricted):
    def __init__(self, count) -> None:
        super().__init__(f"Can't go forward for {count}!")

class CantGoBackward(MoveRestricted):
    def __init__(self, count) -> None:
        super().__init__(f"Can't go backward for {count}!")

class CaseCheck(MoveRestricted):
    def __init__(self) -> None:
        super().__init__(f"Can't move, Kings position under attack")
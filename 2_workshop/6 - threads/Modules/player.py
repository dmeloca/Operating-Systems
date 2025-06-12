VALID_SELECTION: list = ['r', 'p', 's']

class Player:
    def __init__(self, name: str):
        self.name = name
        self._selection = ""

    @property
    def selection(self):
        return self._selection

    @selection.setter
    def selection(self, value):
        if value == 'e':
            raise ValueError("Exit selected")
        elif not self.is_valid_selection(value):
            raise ValueError("Invalid selection. Must be r, p, or s.")
        self._selection = value

    @staticmethod
    def is_valid_selection(selection: str) -> bool:
        return selection in VALID_SELECTION

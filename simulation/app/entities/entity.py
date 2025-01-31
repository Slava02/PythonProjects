import abc
from abc import ABC


class Entity(ABC):
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"






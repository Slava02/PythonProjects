from entity import Entity
class Grass(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, symbol='G')

class Rock(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, symbol='R')

class Tree(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, symbol='G')
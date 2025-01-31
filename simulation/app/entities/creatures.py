from entity import Entity
from abc import ABC

class Creature(Entity, ABC):
    def __init__(self, x, y, symbol, hp, speed):
        super().__init__(x, y, symbol)
        self.hp = hp
        self.speed = speed

    @abc.abstractmethod
    def make_move(self): pass

class Herbivore(Creature):
    def __init__(self, x, y):
        super().__init__(x, y, symbol='H', hp='100', speed='2')

    def make_move(self):
         # Move towards grass

    def eat(self):
        # Eat grass

class Carnivore(Creature):
    def __init__(self, x, y, damage):
        super().__init__(x, y, symbol='C', hp='100', speed='2')
        self.damage = damage

    def make_move(self):
        # Move towards Herbivore

    def attack(self):
        # Attack Herbivore

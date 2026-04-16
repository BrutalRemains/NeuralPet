import unittest
from entity.creature import Creature
# unit testing will mainly look like testing the creature class methods

class TestCreature(unittest.TestCase):
    def setUp(self):
        self.creature = Creature(name="Testy", species="TestSpecies")


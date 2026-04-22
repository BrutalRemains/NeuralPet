import unittest
from entity.creature import Creature, CreatureState
# unit testing will mainly look like testing the creature class methods

class TestCreature(unittest.TestCase):
    def setUp(self):
        self.creature = Creature(name="Testy", species="TestSpecies")
    
    def test_calculate_mood(self):
        self.creature.energy = 20
        self.assertEqual(self.creature.calculate_mood(), CreatureState.TIRED)

        self.creature.energy = 100
        self.creature.fullness = 20
        self.assertEqual(self.creature.calculate_mood(), CreatureState.HUNGRY)

        self.creature.fullness = 100
        self.creature.happiness = 20
        self.assertEqual(self.creature.calculate_mood(), CreatureState.SAD)

        self.creature.happiness = 80
        self.assertEqual(self.creature.calculate_mood(), CreatureState.HAPPY)

        self.creature.happiness = 50
        self.assertEqual(self.creature.calculate_mood(), CreatureState.ANGRY)
    
    def test_prompt_context(self):
        context = self.creature.prompt_context()
        self.assertEqual(context["species"], "TestSpecies")
        self.assertEqual(context["name"], "Testy")
        self.assertEqual(context["age"], 0)
        self.assertEqual(context["mood"], CreatureState.HAPPY.value)
        self.assertEqual(context["energy"], 100)
        self.assertEqual(context["fullness"], 100)
        self.assertEqual(context["happiness"], 100)
        self.assertEqual(context["recent_memories"], "none yet")
        self.assertEqual(context["known_tricks"], "none yet")
        self.assertEqual(context["last_interaction"], self.creature.last_interaction)
    
    

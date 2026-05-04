from datetime import datetime
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
        
    
class TestCreatureMethods(unittest.TestCase): # most methods use basic addition and subtraction, so testing is very straightforward
    def make_creature(**kwargs):
        defaults = dict(
            name="Testy",
            species="TestSpecies",
            age=2,
            energy=80,
            fullness=90,
            happiness=85,
            memory=[],
            known_tricks=[],
            created_at=datetime.now(),
            last_interaction=datetime.now(),
            last_decay_check=datetime.now(),
        )
        defaults.update(kwargs)
        return Creature(**defaults)

    # feed
    def test_feed(self):
        creature = TestCreatureMethods.make_creature(energy=50, fullness=50, happiness=50)
        result = creature.feed()
        self.assertTrue(result["success"])
        self.assertEqual(creature.energy, 50)
        self.assertEqual(creature.fullness, 70)
        self.assertEqual(creature.happiness, 60)

    # play
    def test_play(self):
        creature = TestCreatureMethods.make_creature(energy=80, fullness=90, happiness=100)
        result = creature.play()
        self.assertTrue(result["success"])
        self.assertEqual(creature.energy, 65)
        self.assertEqual(creature.fullness, 80)
        self.assertEqual(creature.happiness, 100)
    
    def test_play_too_tired(self):
        creature = TestCreatureMethods.make_creature(energy=10, fullness=90, happiness=100)
        result = creature.play()
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], "too_tired_to_play")
        self.assertEqual(creature.energy, 10)  # no change
        self.assertEqual(creature.fullness, 90)  # no change
        self.assertEqual(creature.happiness, 100)  # no change
    
    def test_play_too_hungry(self):
        creature = TestCreatureMethods.make_creature(energy=80, fullness=5, happiness=100)
        result = creature.play()
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], "too_hungry_to_play")
        self.assertEqual(creature.energy, 80)  # no change
        self.assertEqual(creature.fullness, 5)  # no change
        self.assertEqual(creature.happiness, 100)  # no change

    # rest
    def test_rest(self):
        creature = TestCreatureMethods.make_creature(energy=50, fullness=90, happiness=100)
        result = creature.rest()
        self.assertTrue(result["success"])
        self.assertEqual(creature.energy, 80)
        self.assertEqual(creature.fullness, 80)
        self.assertEqual(creature.happiness, 100) # no change

    # teach trick
    def test_teach_trick_add_to_known_tricks(self):
        creature = TestCreatureMethods.make_creature(known_tricks=["sit"])
        result = creature.teach_trick("roll over")
        self.assertTrue(result["success"])
        self.assertIn("roll over", creature.known_tricks)
    
    def test_teach_trick_already_known(self):
        creature = TestCreatureMethods.make_creature(known_tricks=["sit"])
        result = creature.teach_trick("sit")
        self.assertFalse(result["success"])
        self.assertIn("sit", creature.known_tricks)
    
    def test_teach_trick_values(self):
        creature = TestCreatureMethods.make_creature(energy=50, happiness=90)
        result = creature.teach_trick("roll over")
        self.assertTrue(result["success"])
        self.assertEqual(creature.energy, 35)
        self.assertEqual(creature.happiness, 100)
    
    def test_teach_trick_insufficient_energy(self):
        creature = TestCreatureMethods.make_creature(energy=10)
        result = creature.teach_trick("roll over")
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], "insufficient_energy")
        self.assertEqual(creature.energy, 10)  # no change

    # perform trick
    def test_perform_trick_success(self):
        creature = TestCreatureMethods.make_creature(known_tricks=["sit"], energy=50, happiness=90)
        result = creature.perform_trick("sit")
        self.assertTrue(result["success"])
        self.assertEqual(creature.happiness, 95)
        self.assertEqual(creature.energy, 45)
    
    def test_perform_trick_not_known(self):
        creature = TestCreatureMethods.make_creature(known_tricks=["sit"], energy=50, happiness=90)
        result = creature.perform_trick("roll over")
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], "trick_not_known")
        self.assertEqual(creature.happiness, 90)  # no change
        self.assertEqual(creature.energy, 50)  # no change
    
    def test_perform_trick_insufficient_energy(self):
        creature = TestCreatureMethods.make_creature(known_tricks=["sit"], energy=3, happiness=90)
        result = creature.perform_trick("sit")
        self.assertFalse(result["success"])
        self.assertEqual(result["reason"], "insufficient_energy")
        self.assertEqual(creature.happiness, 90) # no change
        self.assertEqual(creature.energy, 3)  # no change

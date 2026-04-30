import unittest
from services import prompt_builder

class TestPrompts(unittest.TestCase):
    def test_render_creature_prompt(self):
        context = {
            "species": "TestSpecies",
            "name": "Testy",
            "age": 2,
            "mood": "happy",
            "energy": 80,
            "fullness": 90,
            "happiness": 85,
            "recent_memories": "played fetch, ate a treat",
            "known_tricks": "sit, roll over"
        }
        prompt = prompt_builder.render_creature_prompt(context)
        self.assertIn("TestSpecies", prompt)
        self.assertIn("Testy", prompt)
        self.assertIn("2", prompt)
        self.assertIn("happy", prompt)
        self.assertIn("80", prompt)
        self.assertIn("90", prompt)
        self.assertIn("85", prompt)
        self.assertIn("played fetch, ate a treat", prompt)
        self.assertIn("sit, roll over", prompt)
from entity.creature import Creature
from services.llama import get_llm


def chat():
    running = True
    creature = Creature(name=None, species=None)
    # llm = get_llm()

    while running:
        if creature.name is None:
            print("Hello! Welcome to NeuroPet!")
            print("")
            print("Let's start by creating your creature.")
            print("First, let's choose a species for your creature.")
            print("It can be anything you like! The species you choose will influence your creature's behavior")
            creature.species = input("What species would you like your creature to be? ")
            while creature.species.strip() == "":
                creature.species = input("What species would you like your creature to be? ")
                if creature.species.strip() == "":
                    continue
            creature.name = input("What would you like to name your creature? ")
            while creature.name.strip() == "":
                creature.name = input("What would you like to name your creature? ")
                if creature.name.strip() == "":
                    continue
                
            print(f"Great! You've created a {creature.species} named {creature.name}.")
            print("Now, let's interact with your creature! You can feed it, play with it, or just talk to it.")

        if creature.name is not None:
            print("")
            print("Welcome back to your NeuroPet!")
            print(f"What would you like to do with {creature.name}?")
            print("You can feed it, play with it, or just talk to it.")
            
    


if __name__ == "__main__":
    chat()

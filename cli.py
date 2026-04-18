
from entity.creature import Creature
from services.llama import get_llm
from data.database import save_creature, load_creature, row_to_creature


def chat():
    
    load_creature_data = load_creature()
    
    # llm = get_llm()

    
    if load_creature_data is None:
        print("Hello! Welcome to NeuroPet!")
        print("")
        print("Let's start by creating your creature.")
        print("First, let's choose a species for your creature.")
        print("It can be anything you like! The species you choose will influence your creature's behavior")
        species = input("What species would you like your creature to be? ")
        while species.strip() == "":
            species = input("What species would you like your creature to be? ")
            if species.strip() == "":
                continue
        name = input("What would you like to name your creature? ")
        while name.strip() == "":
            name = input("What would you like to name your creature? ")
            if name.strip() == "":
                continue
            
        print(f"Great! You've created a {species} named {name}.")
        print("Now, let's interact with your creature! You can feed it, play with it, or just talk to it.")

    else:
            creature = row_to_creature(load_creature_data)
    
    running = True
    while running:
        print("")
        
    


if __name__ == "__main__":
    chat()

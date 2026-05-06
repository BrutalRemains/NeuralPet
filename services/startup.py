from data.database import initialize_db, save_creature, load_creature, row_to_creature 
from entity.creature import Creature

# service layer for managing creature-related operations meant to scale with both complexity
# and number of implementations such as web and cli

def create_or_load_creature():
    initialize_db()
    load_creature_data = load_creature()
    if load_creature_data is None:
        return None
    creature = row_to_creature(load_creature_data)
    
    creature.apply_decay()  # apply decay when loading for real-time decay  
    return creature

def create_and_save_creature(name, species):
    creature = Creature(name=name, species=species)
    save_creature(creature)
    return creature

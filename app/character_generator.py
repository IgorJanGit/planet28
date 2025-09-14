# Planet 28 Character Generator

import random
from app.traits_api import list_traits, add_trait_to_character
from app.abilities_api import list_abilities, add_ability_to_character, add_custom_ability

# Core skills
SKILLS = ['Agility', 'Fighting', 'Shooting', 'Awareness', 'Psyche']

# Default starting values
DEFAULT_SKILL = 1
DEFAULT_SPEED = 10
DEFAULT_HITPOINTS = 20

# Example abilities (add more as needed)
ABILITIES = [
    {'name': 'Aimed shot', 'cost': 10, 'effect': '+1D8 damage on next attack.'},
    {'name': 'Heal', 'cost': 20, 'effect': 'Restore 1D6 hit-points to another character.'},
    # ... add more abilities from the rules ...
]

def create_character(name):
    character = {
        'Name': name,
        'Points': 10,  # base cost
        'Skills': {skill: DEFAULT_SKILL for skill in SKILLS},
        'Speed': DEFAULT_SPEED,
        'Hit-points': DEFAULT_HITPOINTS,
        'Traits': [],
        'Abilities': [],
        'Equipment': [],
    }
    return character

def main_menu():
    character = None
    while True:
        print("\n--- Planet 28 Character Generator ---")
        print("1. Create new character")
        print("2. Add trait")
        print("3. Add ability")
        print("4. Add custom weapon")
        print("5. View character sheet")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input('Enter character name: ')
            character = create_character(name)
            print(f"Character '{name}' created.")
        elif choice == '2':
            if not character:
                print("Create a character first.")
                continue
            print("1. Add official trait\n2. Add custom trait")
            sub_choice = input("Choose an option: ")
            if sub_choice == '1':
                traits = list_traits()
                print("Available traits:")
                for idx, trait in enumerate(traits):
                    print(f"{idx+1}. {trait['name']} (Cost: {trait['cost']}) - {trait['effect']}")
                t_choice = input("Select trait number to add: ")
                try:
                    t_idx = int(t_choice) - 1
                    trait = traits[t_idx]
                    added = add_trait_to_character(character, trait['name'])
                    if added:
                        print(f"Trait '{trait['name']}' added.")
                    else:
                        print("Trait already added or not found.")
                except (ValueError, IndexError):
                    print("Invalid choice.")
            elif sub_choice == '2':
                from app.traits_api import add_custom_trait
                name = input("Custom trait name: ")
                try:
                    cost = int(input("Custom trait cost (integer): "))
                except ValueError:
                    print("Invalid cost.")
                    continue
                effect = input("Custom trait effect/description: ")
                added = add_custom_trait(name, cost, effect)
                if added:
                    print(f"Custom trait '{name}' added to the list.")
                else:
                    print("A trait with that name already exists.")
            else:
                print("Invalid option.")
        elif choice == '3':
            if not character:
                print("Create a character first.")
                continue
            print("1. Add official ability\n2. Add custom ability")
            sub_choice = input("Choose an option: ")
            if sub_choice == '1':
                abilities = list_abilities()
                print("Available abilities:")
                for idx, ab in enumerate(abilities):
                    print(f"{idx+1}. {ab['name']} (Cost: {ab['cost']}) - {ab['effect']}")
                a_choice = input("Select ability number to add: ")
                try:
                    a_idx = int(a_choice) - 1
                    ab = abilities[a_idx]
                    added = add_ability_to_character(character, ab['name'])
                    if added:
                        print(f"Ability '{ab['name']}' added.")
                    else:
                        print("Ability already added or not found.")
                except (ValueError, IndexError):
                    print("Invalid choice.")
            elif sub_choice == '2':
                name = input("Custom ability name: ")
                try:
                    cost = int(input("Custom ability cost (integer): "))
                except ValueError:
                    print("Invalid cost.")
                    continue
                effect = input("Custom ability effect/description: ")
                added = add_custom_ability(name, cost, effect)
                if added:
                    print(f"Custom ability '{name}' added to the list.")
                else:
                    print("An ability with that name already exists.")
            else:
                print("Invalid option.")
        elif choice == '4':
            if not character:
                print("Create a character first.")
                continue
            print("-- Custom Weapon Creation --")
            w_name = input("Weapon name: ")
            w_range = int(input("Weapon range (cm, 0 for melee): "))
            w_dice = input("Damage dice (e.g. 2D6+3): ")
            w_max_damage = int(input("Maximum possible damage on a single roll: "))
            w_cost = w_range + w_max_damage
            one_handed = input("One-handed? (y/n): ").lower() == 'y'
            if one_handed:
                w_cost += 10
            # For simplicity, skip special rules for now
            weapon = {
                'name': w_name,
                'range': w_range,
                'damage': w_dice,
                'cost': w_cost,
                'one_handed': one_handed
            }
            character['Equipment'].append(weapon)
            print(f"Weapon '{w_name}' added (Cost: {w_cost} credits).")
        elif choice == '5':
            if not character:
                print("Create a character first.")
                continue
            print("\n--- Character Sheet ---")
            print(f"Name: {character['Name']}")
            print(f"Points cost: {character['Points']}")
            print("Agility  Shooting  Fighting  Psyche  Awareness")
            print("  ".join(str(character['Skills'][k]) for k in ['Agility', 'Shooting', 'Fighting', 'Psyche', 'Awareness']))
            print(f"Speed: {character['Speed']}   Hit-points: {character['Hit-points']}")
            print(f"Traits: {', '.join(character['Traits']) if character['Traits'] else '-'}")
            print(f"Abilities: {', '.join(character['Abilities']) if character['Abilities'] else '-'}")
            if character['Equipment']:
                eq_lines = []
                for eq in character['Equipment']:
                    if isinstance(eq, dict):
                        eq_lines.append(f"{eq['name']} (Range: {eq['range']}cm, Damage: {eq['damage']}, Cost: {eq['cost']}{', One-handed' if eq.get('one_handed') else ''})")
                    else:
                        eq_lines.append(str(eq))
                print(f"Equipment: {', '.join(eq_lines)}")
            else:
                print("Equipment: -")
            print("Injuries: -")
            print("Campaign points: -")
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == '__main__':
    main_menu()

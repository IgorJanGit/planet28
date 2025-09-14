# abilities_api.py
"""
API for Planet 28 character abilities.
"""

ABILITIES = [
    {"name": "Aimed shot", "cost": 10, "effect": "Use an action to aim at an enemy's weak spot. Weapon does +1D8 damage on next attack this turn."},
    {"name": "Drain", "cost": 25, "effect": "Remove 1 hit-point from any character within 5cm and add it to own hit-points."},
    {"name": "Heal", "cost": 20, "effect": "Restore 1D6 hit-points to any other character in base contact."},
    {"name": "Haggle", "cost": 30, "effect": "Haggle price of items in off-table games. Roll 1D6: 1-3 reduce by 1D4 credits, 4-6 by 1D10. Price can't go below 1 credit."},
    {"name": "Inspire", "cost": 25, "effect": "A chosen friendly character in line of sight gets +1D6 to skills for the rest of the turn."},
    {"name": "Loot", "cost": 30, "effect": "Once per game, after slaying an enemy in combat, take one piece of equipment from them permanently."},
    {"name": "Persuade", "cost": 25, "effect": "In combat, make a (P) roll. If successful, both break from combat and can't attack each other for the rest of the turn."},
    {"name": "Repair", "cost": 15, "effect": "In base contact with a vehicle, restore 1D8 hit-points to any section, regardless of facing."},
    {"name": "Sabotage", "cost": 20, "effect": "Within 5cm of enemy vehicle, choose a section from a random facing. That section is destroyed for 1D6 turns, then returns to normal."},
    {"name": "Throw", "cost": 15, "effect": "Throw any character in base contact 1D12cm in a straight line. Characters thrown off ledges take fall damage."},
]

def list_abilities():
    """Return all abilities."""
    return ABILITIES

def get_ability(name):
    """Get an ability by name (case-insensitive)."""
    for ab in ABILITIES:
        if ab["name"].lower() == name.lower():
            return ab
    return None

def add_ability_to_character(character, ability_name):
    """Add an ability to a character, updating points and abilities list."""
    ab = get_ability(ability_name)
    if ab and ab["name"] not in character["Abilities"]:
        character["Abilities"].append(ab["name"])
        character["Points"] += ab["cost"]
        return True
    return False

def add_custom_ability(name, cost, effect):
    """Add a custom ability to the ability list for this session."""
    ab = {"name": name, "cost": cost, "effect": effect}
    if not any(a["name"].lower() == name.lower() for a in ABILITIES):
        ABILITIES.append(ab)
        return True
    return False

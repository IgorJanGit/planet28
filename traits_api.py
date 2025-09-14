# traits_api.py
"""
API for Planet 28 character traits.
"""

TRAITS = [
    {"name": "Ammo smith", "cost": 15, "effect": "After each game this character may craft 1 piece of ammo for any weapon of their choice. This is automatically added to their equipment."},
    {"name": "Animal", "cost": -20, "effect": "Cannot use abilities or shoot. -1(P) during break tests."},
    {"name": "Armless", "cost": -20, "effect": "Missing an arm. May only wield a single 1 handed weapon or use a single item at any time."},
    {"name": "Blessed", "cost": 50, "effect": "Roll 2D10 for all skill rolls and keep the lowest score."},
    {"name": "Big", "cost": 8, "effect": "+1(F) when charging. -3cm speed."},
    {"name": "Bulwark", "cost": 10, "effect": "Enemies do not receive the standard +1D4(F) when charging this character."},
    {"name": "Brawler", "cost": 9, "effect": "Fists do an additional +1D6 damage."},
    {"name": "Brave", "cost": 15, "effect": "May reroll 1 failed break test per turn."},
    {"name": "Barbaric", "cost": -10, "effect": "Immune to Persuade. Cannot wield weapons/armour with Complex keyword."},
    {"name": "Cursed", "cost": -50, "effect": "Roll 2D10 for all skill rolls and keep the highest score."},
    {"name": "Coward", "cost": -15, "effect": "Must make a break test when charged and may not charge others."},
    {"name": "Climber", "cost": 5, "effect": "+2(A) when climbing any vertical surface."},
    {"name": "Deathproof", "cost": 25, "effect": "On injury table, treat Dead as Complete recovery."},
    {"name": "Extra limbs", "cost": 25, "effect": "May wield 4 single handed or 2 double handed weapons at once."},
    {"name": "Engineer", "cost": 12, "effect": "When in vehicle, restore 1D4 HP per turn to damaged sections in same facing."},
    {"name": "Fast", "cost": 6, "effect": "At start of turn, roll 1D6 and add to speed for that turn."},
    {"name": "Fearless", "cost": 12, "effect": "Immune to Fearsome and Terrifying traits."},
    {"name": "Fearsome", "cost": 12, "effect": "Enemies must pass break test to charge this character."},
    {"name": "Foul aura", "cost": 15, "effect": "Enemies in base contact take 1 damage per turn."},
    {"name": "Gigantic", "cost": 18, "effect": "All effects of Big, not in cover unless completely obscured, cannot be pushed back, only takes fall damage from 20cm+."},
    {"name": "Gunner", "cost": 10, "effect": "When in vehicle, may act as crew for shooting. Uses own shooting skill."},
    {"name": "Gunslinger", "cost": 20, "effect": "May make shoot actions when locked in combat."},
    {"name": "Intelligent", "cost": 10, "effect": "May reroll one failed (AW) roll per turn."},
    {"name": "Incorporeal", "cost": 15, "effect": "May move through obstacles/characters as if even ground."},
    {"name": "Inspiring", "cost": 25, "effect": "Friendly characters within 10cm get +1 to skills."},
    {"name": "Iron skin", "cost": 8, "effect": "May make an additional 1D4 armour roll when taking damage."},
    {"name": "Major arcana", "cost": 30, "effect": "May perform arcana abilities (roll 3 random at start of game, use any number of times)."},
    {"name": "Medic", "cost": 15, "effect": "May heal one injury from any friendly character between games (cannot do anything else that time)."},
    {"name": "Mercenary", "cost": -5, "effect": "Must be paid 10 credits before each game or cannot join. May convert campaign points to credits 1:1."},
    {"name": "Minor arcana", "cost": 18, "effect": "May perform arcane abilities (roll 1 random at start of game, use any number of times)."},
    {"name": "Mysterious motives", "cost": 6, "effect": "At start of turn, roll 1D10 for (A) activation."},
    {"name": "Painless", "cost": 25, "effect": "On injury table, all injuries except Death are Complete recovery."},
    {"name": "Pilot", "cost": 15, "effect": "When in vehicle, vehicle may use this character's agility and shooting values."},
    {"name": "Psychic", "cost": 18, "effect": "May reroll a failed arcana ability once per turn."},
    {"name": "Rich", "cost": 28, "effect": "Gains +1D8 credits after each game."},
    {"name": "Rageful", "cost": -10, "effect": "May never leave combat. Fights until dead or opponent leaves/dies."},
    {"name": "slow", "cost": -6, "effect": "At start of turn, roll 1D6 and remove from speed for that turn."},
    {"name": "Sniper", "cost": 17, "effect": "May reroll any failed Shooting rolls once."},
    {"name": "Sure-footed", "cost": 10, "effect": "Treats rough ground as even, hazardous as rough."},
    {"name": "Stupid", "cost": -10, "effect": "Must roll all (P) rolls twice, taking the worse result."},
    {"name": "Tank hunter", "cost": 15, "effect": "+1 Shooting when shooting at a vehicle."},
    {"name": "Terrifying", "cost": 30, "effect": "Enemies must pass break test to charge, attack, or shoot at this character. NPCs are hostile in off-table games."},
    {"name": "Unshakable", "cost": 25, "effect": "Never needs to take a break test."},
    {"name": "Unbreakable conviction", "cost": 20, "effect": "Immune to Persuade and Mind control. All friendlies within 10cm are also immune."},
    {"name": "Unearthly", "cost": 40, "effect": "Can only be damaged by weapons with Psychic, Arcane, or Demonic keyword."},
    {"name": "Venal", "cost": -12, "effect": "Must always convert spare campaign points to credits, cannot save campaign points."},
    {"name": "Zealot", "cost": 15, "effect": "Whenever this character takes damage, roll 1D10. On a 10, gain +1 (F) and (A) for the rest of the game (max 10)."},
]

def list_traits():
    """Return all traits."""
    return TRAITS

def get_trait(name):
    """Get a trait by name (case-insensitive)."""
    for trait in TRAITS:
        if trait["name"].lower() == name.lower():
            return trait
    return None

def add_trait_to_character(character, trait_name):
    """Add a trait to a character, updating points and traits list."""
    trait = get_trait(trait_name)
    if trait and trait["name"] not in character["Traits"]:
        character["Traits"].append(trait["name"])
        character["Points"] += trait["cost"]
        return True
    return False

def add_custom_trait(name, cost, effect):
    """Add a custom trait to the trait list for this session."""
    trait = {"name": name, "cost": cost, "effect": effect}
    # Prevent duplicates by name
    if not any(t["name"].lower() == name.lower() for t in TRAITS):
        TRAITS.append(trait)
        return True
    return False

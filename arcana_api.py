# arcana_api.py
"""
API for Planet 28 arcane (arcana) abilities.
"""

ARCANA = [
    {"roll": 1, "name": "Blind", "effect": "Make a (P) roll. If successful, all characters and vehicles within 15cm cannot make any actions for the remainder of the turn."},
    {"roll": 2, "name": "Smite", "effect": "Select a character or vehicle in line of sight and make a (P) roll. If successful, that target takes 1D10+5 damage. Target may make an armour roll."},
    {"roll": 3, "name": "Terrify", "effect": "Select a character in line of sight and make a (P) roll. If successful, that character must immediately retreat to the nearest table edge as if they failed a break test."},
    {"roll": 4, "name": "Rend the earth", "effect": "Select a character in line of sight and make a (P) roll. If successful, all terrain within 20cm of that character counts as hazardous terrain for the rest of the game."},
    {"roll": 5, "name": "Mind control", "effect": "Select a character in line of sight and make a (P) roll. If successful, the acting character may make one additional action with the chosen character. This action does not count as one of the target's usual actions."},
    {"roll": 6, "name": "Wither", "effect": "Select a character in line of sight and make a (P) roll. If successful, that character suffers –1D4 to their skills for 1D6 turns."},
    {"roll": 7, "name": "Flame", "effect": "Make a (P) roll. If successful, 1 character in line of sight suffers 1D8 damage. The affected character must use an action to extinguish the flame or suffer 1D4 damage for every turn they fail to do so. This damage cannot be stopped by armour."},
    {"roll": 8, "name": "Summon", "effect": "Select a character in line of sight and make a (P) roll. If successful, place an exact duplicate of that character anywhere on the board and control them for the next 1D4 turns, after which they disappear. Casting this spell is at –2(P)."},
    {"roll": 9, "name": "Shield", "effect": "Select a friendly character anywhere on the tabletop and make a (P) roll. If successful, the target may not be targeted by ranged or melee attacks for the rest of the turn."},
    {"roll": 10, "name": "Teleport", "effect": "Make a (P) roll and select any part of the playing area within line of sight. If successful, move this character there immediately."},
    {"roll": 11, "name": "Dishearten", "effect": "Select a character in line of sight and make a (P) roll. If successful, that character acts last in the next turn, regardless of their (A) score."},
    {"roll": 12, "name": "Immobilize", "effect": "Select a character in line of sight and make a (P) roll. If successful, that character may not move for 1D4 turns."},
]

def list_arcana():
    """Return all arcane abilities."""
    return ARCANA

def get_arcana_by_roll(roll):
    """Get arcane ability by 1D12 roll."""
    for arc in ARCANA:
        if arc["roll"] == roll:
            return arc
    return None

def get_arcana_by_name(name):
    """Get arcane ability by name (case-insensitive)."""
    for arc in ARCANA:
        if arc["name"].lower() == name.lower():
            return arc
    return None

def add_custom_arcana(name, effect):
    """Add a custom arcane ability to the list for this session."""
    if not any(a["name"].lower() == name.lower() for a in ARCANA):
        ARCANA.append({"roll": len(ARCANA)+1, "name": name, "effect": effect})
        return True
    return False

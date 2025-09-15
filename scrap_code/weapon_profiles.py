"""
This module contains code for processing weapon profiles and special rules
for display on the character sheet with collapsible sections.

This code was used to:
1. Expand weapon data with detailed information
2. Process special rules to remove cost information
3. Provide formatted weapon data to the character sheet template
"""

import re
import json
import os

def get_weapon_profiles_for_character(character):
    """
    Get detailed weapon profiles for a character, with special rules expanded
    and cost information removed from the descriptions.
    
    Args:
        character (dict): The character data
        
    Returns:
        list: A list of weapon profile dictionaries with expanded special rules
    """
    from app.weapons_api import get_weapon, get_special_rules
    
    weapon_profiles = []
    special_rules_dict = get_special_rules()
    
    for weapon_name in character.get('Weapons', []):
        weapon_data = get_weapon(weapon_name)
        if weapon_data:
            # Add special rules descriptions to each weapon
            if weapon_data.get('special_rules'):
                rules_with_desc = []
                for rule in [r.strip() for r in weapon_data['special_rules'].split(',') if r.strip()]:
                    # Get the description and remove the cost information
                    description = special_rules_dict.get(rule, 'No description available')
                    # Remove cost information (anything like (+XX cost) or (-XX cost))
                    description = re.sub(r'\([+\-]\d+\s+cost\)', '', description).strip()
                    
                    rules_with_desc.append({
                        'name': rule,
                        'description': description
                    })
                weapon_data['special_rules_expanded'] = rules_with_desc
            weapon_profiles.append(weapon_data)
    
    return weapon_profiles
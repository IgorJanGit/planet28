# Scrap Code - Weapon Profiles

This directory contains code that was developed to show detailed weapon profiles on the character sheet.

## Features that were implemented

1. **Detailed Weapon Display**
   - Enhanced display of weapons on the character sheet
   - Table showing Type, Size, Damage, Range, and Cost
   - Collapsible special rules section

2. **Special Rules Processing**
   - Expanded weapon special rules with descriptions
   - Removed cost information from special rule descriptions
   - Added collapsible UI for rules with toggle indicators

3. **CSS Styling**
   - Grid-based layout for weapon stats
   - Styled tables with proper borders
   - Responsive collapsible sections

## Files

- **weapon_profiles.css**: CSS styles for the enhanced weapon display
- **weapon_profiles.py**: Python code for processing weapon data and special rules
- **weapon_profiles_template.html**: HTML template code for the detailed weapon display

## Why this code was removed

This code was developed as a prototype but ultimately not used in the final implementation. It has been saved here for future reference in case these features are needed later.

## How to reimplement

To reimplement these features:

1. Copy the CSS file to `/static/css/`
2. Add the CSS link to the head of edit_character.html
3. Add the Python code to the edit_character_get function in main.py
4. Replace the simple weapon list in edit_character.html with the weapon_profiles_template.html code
5. Make sure the JavaScript for collapsible functionality is included
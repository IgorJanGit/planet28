# Planet 28 Character Generator Web App

## Overview
This project is a web-based character and warband manager for the Planet 28 tabletop game. It is built with Python, FastAPI, Jinja2 templates, HTML/CSS, and JavaScript. The app allows users to create, edit, and manage warbands, characters, vehicles, traits, abilities, and more.

## Project Structure & UI Organization
- **Backend:** Python (FastAPI)
  - All API routes and business logic are in `main.py` and modular API files (e.g., `traits_api.py`, `abilities_api.py`, `weapons_api.py`).
  - Data is stored as JSON files in warband-named folders.
  - Real-time calculations via API endpoints for dynamic point updates.
- **Frontend:** Jinja2 templates, HTML, CSS, JavaScript
  - UI templates are in the `templates/` folder.
  - Client-side JavaScript for real-time updates and dynamic content.
  - API-based point calculation for instant feedback on character changes.

## Main Flows
### 1. Create/Edit Character
- User selects a warband and character or creates a new one.
- The edit form allows:
  - Editing stats, points, and notes.
  - Adding/removing traits and abilities (with description toggles and previews).
  - Adding/removing weapons with special rules and automatic point cost calculation.
  - Editing equipment, injuries, and campaign points.
- Real-time point calculation updates as changes are made.
- All changes are saved to the character's JSON file.

### 2. Warband Management
- Create and manage multiple warbands.
- Toggle homebrew mode at the warband level to enforce or relax game rules.
- Track total points across all characters in a warband.

### 3. Export/Print
- User can export a character or warband sheet to a printable format.
- Export uses a dedicated template for clean print layout.

## UI/UX Organization
- The UI is organized into clear sections: stats, traits, abilities, equipment, etc.
- Traits and abilities can be added/removed dynamically with buttons and dropdowns.
- Description toggles and previews help users understand effects before adding.
- The layout is responsive and contained within a styled box for clarity.

## Current Status
- **UI and create/export flows are complete and visually organized.**
- **Character creation, trait and ability management, point calculations, and weapon systems are fully functional.**
- **Homebrew mode toggle allows for flexible character creation with or without rule restrictions.**
- Equipment, injuries, and campaign points features are completed.

## Features
### Skill System
- Characters have 5 core skills: Agility, Shooting, Fighting, Psyche, and Awareness.
- Each skill level above 1 costs 10 points.
- When homebrew mode is disabled, skills are capped at 10.

### Hit-Points System
- Every character starts with 20 hit-points.
- Characters can increase their hit-points by 2 for a cost of 10 points.
- Characters can decrease their hit-points by 2 for a savings of 10 points.

### Speed System
- Every character starts with a speed of 10cm.
- In standard mode, speed cannot be changed with points.
- In homebrew mode, speed can be modified at a cost of 10 points per point of speed.

### Weapon System
- Comprehensive weapon database with various weapon types (Melee, Ranged, etc.).
- Each weapon has attributes: damage, range, special rules, and point cost.
- Weapon costs are automatically added to the character's total point cost.
- Special rules for weapons have detailed descriptions in a reference page.
- Real-time point calculation updates when weapons are added or removed.

## Next Steps
- Enhance the campaign management system.
- Add more detailed vehicle management.
- Improve printing and export options.
- Add user authentication and cloud saving.

## How to Run
1. Install dependencies: `pip install fastapi uvicorn jinja2`
2. Start the server: `uvicorn main:app --reload`
3. Open your browser to `http://127.0.0.1:8000/`

---
**Note:** This README reflects the current state: UI and export are visually complete, but some interactive logic is broken and needs fixing.

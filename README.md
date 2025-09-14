# Planet 28 Character Generator Web App

## Overview
This project is a web-based character and warband manager for the Planet 28 tabletop game. It is built with Python, FastAPI, Jinja2 templates, HTML/CSS, and JavaScript. The app allows users to create, edit, and manage warbands, characters, vehicles, traits, abilities, and more.

## Project Structure & UI Organization
- **Backend:** Python (FastAPI)
  - All API routes and business logic are in `main.py` and modular API files (e.g., `traits_api.py`, `abilities_api.py`).
  - Data is stored as JSON files in warband-named folders.
- **Frontend:** Jinja2 templates, HTML, CSS, JavaScript
  - UI templates are in the `templates/` folder.
  - The main flows are:
    - **Dashboard:** View and manage warbands and their characters/vehicles.
    - **Edit Character:** Form to edit all character stats, traits, abilities, equipment, etc.
    - **Export/Print:** Export a printable character or warband sheet.

## Main Flows
### 1. Create/Edit Character
- User selects a warband and character or creates a new one.
- The edit form allows:
  - Editing stats, points, and notes.
  - Adding/removing traits and abilities (with description toggles and previews).
  - Editing equipment, injuries, and campaign points (some features in development).
- All changes are saved to the character's JSON file.

### 2. Export/Print
- User can export a character or warband sheet to a printable format.
- Export uses a dedicated template for clean print layout.

## UI/UX Organization
- The UI is organized into clear sections: stats, traits, abilities, equipment, etc.
- Traits and abilities can be added/removed dynamically with buttons and dropdowns.
- Description toggles and previews help users understand effects before adding.
- The layout is responsive and contained within a styled box for clarity.

## Current Status
- **UI and create/export flows are complete and visually organized.**
- **Logical and functional code for adding/removing traits and abilities is currently broken or unreliable.**
  - Add/remove buttons may not work as expected due to JavaScript or template issues.
  - Some features (equipment, injuries, campaign points) are still in development.

## Next Steps
- Fix and robustly test all add/remove logic for traits and abilities.
- Complete equipment and campaign management features.
- Improve error handling and validation.

## How to Run
1. Install dependencies: `pip install fastapi uvicorn jinja2`
2. Start the server: `uvicorn main:app --reload`
3. Open your browser to `http://127.0.0.1:8000/`

---
**Note:** This README reflects the current state: UI and export are visually complete, but some interactive logic is broken and needs fixing.

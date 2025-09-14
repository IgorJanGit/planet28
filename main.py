

# ...existing code...


from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import json
import shutil
from app.traits_api import list_traits, get_trait
from app.abilities_api import list_abilities, get_ability
from app.arcana_api import list_arcana

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Delete a warband and all its contents
@app.post("/delete_warband")
def delete_warband(warband_name: str = Form(...)):
    path = os.path.join(WARBANDS_DIR, warband_name)
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
    return RedirectResponse("/warbands", status_code=303)

# In-memory character for demo
CHARACTER = {
    'Name': '',
    'Points': 10,
    'Skills': {'Agility': 1, 'Fighting': 1, 'Shooting': 1, 'Awareness': 1, 'Psyche': 1},
    'Speed': 10,
    'Hit-points': 20,
    'Traits': [],
    'Abilities': [],
    'Equipment': [],
}

WARBANDS_DIR = "warbands"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Redirect to warbands selection if no warband is selected
    warband = request.cookies.get("warband")
    if not warband:
        return RedirectResponse("/warbands", status_code=303)

    # Get full trait/ability objects for display
    trait_objs = [get_trait(t) for t in CHARACTER['Traits']]
    ability_objs = [get_ability(a) for a in CHARACTER['Abilities']]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "character": CHARACTER,
            "trait_objs": trait_objs,
            "ability_objs": ability_objs,
        },
    )

@app.post("/set_name")
def set_name(name: str = Form(...)):
    CHARACTER['Name'] = name
    return RedirectResponse("/", status_code=303)

@app.post("/set_points")
def set_points(points: int = Form(...)):
    CHARACTER['Points'] = points
    return RedirectResponse("/", status_code=303)

@app.get("/traits", response_class=HTMLResponse)
def traits(request: Request):
    return templates.TemplateResponse("traits.html", {"request": request, "traits": list_traits(), "character": CHARACTER})

@app.post("/add_trait")
def add_trait(trait: str = Form(...)):
    if trait not in CHARACTER['Traits']:
        CHARACTER['Traits'].append(trait)
    return RedirectResponse("/traits", status_code=303)

@app.post("/remove_trait")
def remove_trait(trait: str = Form(...)):
    if trait in CHARACTER['Traits']:
        CHARACTER['Traits'].remove(trait)
    return RedirectResponse("/", status_code=303)

@app.get("/abilities", response_class=HTMLResponse)
def abilities(request: Request):
    return templates.TemplateResponse("abilities.html", {"request": request, "abilities": list_abilities(), "character": CHARACTER})

@app.post("/add_ability")
def add_ability(ability: str = Form(...)):
    if ability not in CHARACTER['Abilities']:
        CHARACTER['Abilities'].append(ability)
    return RedirectResponse("/abilities", status_code=303)

@app.post("/remove_ability")
def remove_ability(ability: str = Form(...)):
    if ability in CHARACTER['Abilities']:
        CHARACTER['Abilities'].remove(ability)
    return RedirectResponse("/", status_code=303)

@app.get("/arcana", response_class=HTMLResponse)
def arcana(request: Request):
    return templates.TemplateResponse("arcana.html", {"request": request, "arcana": list_arcana(), "character": CHARACTER})

@app.post("/remove_equipment")
def remove_equipment(eq_name: str = Form(...)):
    # Remove by name (works for both dict and str equipment)
    CHARACTER['Equipment'] = [eq for eq in CHARACTER['Equipment'] if not ((isinstance(eq, dict) and eq.get('name') == eq_name) or (isinstance(eq, str) and eq == eq_name))]
    return RedirectResponse("/", status_code=303)

@app.get("/export", response_class=HTMLResponse)
def export(request: Request):
    trait_objs = [get_trait(t) for t in CHARACTER['Traits']]
    ability_objs = [get_ability(a) for a in CHARACTER['Abilities']]
    return templates.TemplateResponse(
        "export.html",
        {
            "request": request,
            "character": CHARACTER,
            "trait_objs": trait_objs,
            "ability_objs": ability_objs,
        },
    )

@app.get("/warbands", response_class=HTMLResponse)
def warbands(request: Request):
    warbands = [d for d in os.listdir(WARBANDS_DIR) if os.path.isdir(os.path.join(WARBANDS_DIR, d))]
    return templates.TemplateResponse("warbands.html", {"request": request, "warbands": warbands})

@app.post("/create_warband")
def create_warband(warband_name: str = Form(...)):
    path = os.path.join(WARBANDS_DIR, warband_name)
    os.makedirs(path, exist_ok=True)
    return RedirectResponse("/warbands", status_code=303)


def _safe_cookie_key(warband):
    # Only allow alphanum and underscores in cookie keys
    return "warband_points_" + "".join(c if c.isalnum() else "_" for c in warband)

@app.get("/warband/{warband}", response_class=HTMLResponse)
def warband_dashboard(request: Request, warband: str):
    wb_path = os.path.join(WARBANDS_DIR, warband)
    chars = []
    vehicles = []
    total_points_spent = 0
    if os.path.exists(wb_path):
        chars = [f[:-5] for f in os.listdir(wb_path) if f.endswith('.json') and not f.startswith('vehicle_')]
        vehicles = [f[8:-5] for f in os.listdir(wb_path) if f.startswith('vehicle_') and f.endswith('.json')]
        # Sum points for all characters
        for char_name in chars:
            char_file = os.path.join(wb_path, f"{char_name}.json")
            try:
                with open(char_file, 'r') as f:
                    char_data = json.load(f)
                    total_points_spent += int(char_data.get('Points', 0))
            except Exception:
                pass
    cookie_key = _safe_cookie_key(warband)
    warband_points = request.cookies.get(cookie_key)
    try:
        warband_points = int(warband_points)
    except (TypeError, ValueError):
        warband_points = 500
    return templates.TemplateResponse("warband_dashboard.html", {"request": request, "warband": warband, "characters": chars, "vehicles": vehicles, "warband_points": warband_points, "total_points_spent": total_points_spent})

# Set warband points limit
@app.post("/set_warband_points/{warband}")
def set_warband_points(request: Request, warband: str, points: int = Form(...)):
    cookie_key = _safe_cookie_key(warband)
    response = RedirectResponse(f"/warband/{warband}", status_code=303)
    response.set_cookie(key=cookie_key, value=str(points))
    return response

@app.post("/add_character")
def add_character(request: Request, char_name: str = Form(...)):
    warband = request.cookies.get("warband")
    if not warband:
        return RedirectResponse("/warbands", status_code=303)
    wb_path = os.path.join(WARBANDS_DIR, warband)
    os.makedirs(wb_path, exist_ok=True)
    char_file = os.path.join(wb_path, f"{char_name}.json")
    # Minimal character stub
    char_data = {
        'Name': char_name,
        'Points': 10,
        'Skills': {'Agility': 1, 'Fighting': 1, 'Shooting': 1, 'Awareness': 1, 'Psyche': 1},
        'Speed': 10,
        'Hit-points': 20,
        'Traits': [],
        'Abilities': [],
        'Equipment': [],
    }
    with open(char_file, 'w') as f:
        json.dump(char_data, f)
    return RedirectResponse(f"/warband/{warband}", status_code=303)

@app.post("/add_vehicle")
def add_vehicle(request: Request, vehicle_name: str = Form(...)):
    warband = request.cookies.get("warband")
    if not warband:
        return RedirectResponse("/warbands", status_code=303)
    wb_path = os.path.join(WARBANDS_DIR, warband)
    os.makedirs(wb_path, exist_ok=True)
    vehicle_file = os.path.join(wb_path, f"vehicle_{vehicle_name}.json")
    # Minimal vehicle stub
    vehicle_data = {
        'Name': vehicle_name,
        'Type': '',
        'Traits': [],
        'Abilities': [],
        'Sections': [],
    }
    with open(vehicle_file, 'w') as f:
        json.dump(vehicle_data, f)
    return RedirectResponse(f"/warband/{warband}", status_code=303)

@app.post("/remove_character")
def remove_character(request: Request, char_name: str = Form(...)):
    warband = request.cookies.get("warband")
    if not warband:
        return RedirectResponse("/warbands", status_code=303)
    wb_path = os.path.join(WARBANDS_DIR, warband)
    char_file = os.path.join(wb_path, f"{char_name}.json")
    if os.path.exists(char_file):
        os.remove(char_file)
    return RedirectResponse(f"/warband/{warband}", status_code=303)

@app.post("/remove_vehicle")
def remove_vehicle(request: Request, vehicle_name: str = Form(...)):
    warband = request.cookies.get("warband")
    if not warband:
        return RedirectResponse("/warbands", status_code=303)
    wb_path = os.path.join(WARBANDS_DIR, warband)
    vehicle_file = os.path.join(wb_path, f"vehicle_{vehicle_name}.json")
    if os.path.exists(vehicle_file):
        os.remove(vehicle_file)
    return RedirectResponse(f"/warband/{warband}", status_code=303)

@app.get("/export_warband/{warband}", response_class=HTMLResponse)
def export_warband(request: Request, warband: str):
    wb_path = os.path.join(WARBANDS_DIR, warband)
    chars = []
    vehicles = []
    if os.path.exists(wb_path):
        for f in os.listdir(wb_path):
            if f.endswith('.json'):
                with open(os.path.join(wb_path, f), 'r') as file:
                    data = json.load(file)
                    if f.startswith('vehicle_'):
                        vehicles.append(data)
                    else:
                        chars.append(data)
    return templates.TemplateResponse("export_warband.html", {"request": request, "warband": warband, "characters": chars, "vehicles": vehicles})



# --- Character Edit Routes ---
@app.get("/edit_character/{warband}/{char_name}", response_class=HTMLResponse)
def edit_character_get(request: Request, warband: str, char_name: str):
    wb_path = os.path.join(WARBANDS_DIR, warband)
    char_file = os.path.join(wb_path, f"{char_name}.json")
    if not os.path.exists(char_file):
        return RedirectResponse(f"/warband/{warband}", status_code=303)
    with open(char_file, "r") as f:
        character = json.load(f)
    traits = list_traits()
    abilities = list_abilities()
    # --- Apply stat modifiers from traits and abilities ---
    from app.traits_api import get_trait
    from app.abilities_api import get_ability
    base_skills = character['Skills'].copy()
    mod_skills = base_skills.copy()
    # Sum modifiers from all traits
    for t in character.get('Traits', []):
        trait = get_trait(t)
        for stat, mod in trait.get('modifiers', {}).items():
            if stat in mod_skills:
                mod_skills[stat] += mod
    # Sum modifiers from all abilities
    for a in character.get('Abilities', []):
        ab = get_ability(a)
        for stat, mod in ab.get('modifiers', {}).items():
            if stat in mod_skills:
                mod_skills[stat] += mod
    # Get warband points limit
    cookie_key = _safe_cookie_key(warband)
    warband_points = request.cookies.get(cookie_key)
    try:
        warband_points = int(warband_points)
    except (TypeError, ValueError):
        warband_points = 500
    # Pass both base and modified skills to template
    return templates.TemplateResponse(
        "edit_character.html",
        {"request": request, "warband": warband, "character": character, "traits": traits, "abilities": abilities, "warband_points": warband_points, "mod_skills": mod_skills}
    )

@app.post("/edit_character/{warband}/{char_name}")
async def edit_character_post(request: Request, warband: str, char_name: str):
    form = await request.form()
    wb_path = os.path.join(WARBANDS_DIR, warband)
    char_file = os.path.join(wb_path, f"{char_name}.json")
    if not os.path.exists(char_file):
        return RedirectResponse(f"/warband/{warband}", status_code=303)
    with open(char_file, "r") as f:
        character = json.load(f)
    # Update fields from form
    character['Name'] = form.get('Name', character['Name'])
    # Recalculate points: base 10 + trait/ability costs
    from app.traits_api import list_traits
    from app.abilities_api import list_abilities
    trait_costs = {t['name']: t['cost'] for t in list_traits()}
    ability_costs = {a['name']: a['cost'] for a in list_abilities()}
    traits = form.get('Traits', '')
    abilities = form.get('Abilities', '')
    equipment = form.get('Equipment', '')
    trait_list = [t.strip() for t in traits.split(',') if t.strip()]
    ability_list = [a.strip() for a in abilities.split(',') if a.strip()]
    # Remove duplicates
    trait_list = list(dict.fromkeys(trait_list))
    ability_list = list(dict.fromkeys(ability_list))
    points = 10
    for t in trait_list:
        points += trait_costs.get(t, 0)
    for a in ability_list:
        points += ability_costs.get(a, 0)
    character['Points'] = points
    character['Skills']['Agility'] = int(form.get('Agility', character['Skills']['Agility']))
    character['Skills']['Shooting'] = int(form.get('Shooting', character['Skills']['Shooting']))
    character['Skills']['Fighting'] = int(form.get('Fighting', character['Skills']['Fighting']))
    character['Skills']['Psyche'] = int(form.get('Psyche', character['Skills']['Psyche']))
    character['Skills']['Awareness'] = int(form.get('Awareness', character['Skills']['Awareness']))
    character['Speed'] = int(form.get('Speed', character['Speed']))
    character['Hit-points'] = int(form.get('Hitpoints', character['Hit-points']))
    character['Traits'] = trait_list
    character['Abilities'] = ability_list
    character['Equipment'] = [e.strip() for e in equipment.split(',') if e.strip()]
    # Save notes/background
    character['Notes'] = form.get('Notes', character.get('Notes', ''))
    # Save back to file (rename if name changed)
    new_name = character['Name']
    new_char_file = os.path.join(wb_path, f"{new_name}.json")
    with open(new_char_file, "w") as f:
        json.dump(character, f)
    if new_char_file != char_file and os.path.exists(char_file):
        os.remove(char_file)
    return RedirectResponse(f"/warband/{warband}", status_code=303)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

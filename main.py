

# ...existing code...


from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import json
import shutil
import datetime
from app.traits_api import list_traits, get_trait
from app.abilities_api import list_abilities, get_ability
from app.arcana_api import list_arcana
from app.weapons_api import list_weapons, get_weapon_types, get_special_rules

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Global config 
def get_global_config():
    config_path = "config.json"
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                # Ensure boolean conversion for homebrew_enabled
                if "homebrew_enabled" in config:
                    if isinstance(config["homebrew_enabled"], str):
                        config["homebrew_enabled"] = config["homebrew_enabled"].lower() == "true"
                    else:
                        config["homebrew_enabled"] = bool(config["homebrew_enabled"])
                return config
        except Exception as e:
            print(f"Error reading global config: {e}")
    return {"homebrew_enabled": False}

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
    # Check if a specific warband and character are provided in the URL query parameters
    params = request.query_params
    warband_param = params.get("warband")
    character_param = params.get("character")
    
    # If specific parameters are provided, use them
    if warband_param and character_param:
        return RedirectResponse(f"/edit_character/{warband_param}/{character_param}", status_code=303)
    
    # Otherwise try to get warband and character from cookies
    warband = request.cookies.get("warband")
    character_name = request.cookies.get("character")
    
    # If both exist, redirect to edit_character
    if warband and character_name:
        return RedirectResponse(f"/edit_character/{warband}/{character_name}", status_code=303)
    
    # If only warband exists, redirect to warband dashboard
    if warband:
        # Check if there are any characters in this warband
        wb_path = os.path.join(WARBANDS_DIR, warband)
        if os.path.exists(wb_path):
            characters = [f.replace(".json", "") for f in os.listdir(wb_path) 
                         if f.endswith(".json") and not f.startswith("vehicle_") and not f == "warband_config.json"]
            if characters:
                # Redirect to the first character's edit page
                return RedirectResponse(f"/edit_character/{warband}/{characters[0]}", status_code=303)
    
    # As a last resort, redirect to warbands selection
    return RedirectResponse("/warbands", status_code=303)

@app.post("/set_name")
def set_name(name: str = Form(...)):
    # Deprecated - kept for reference but redirects to home which will further redirect to edit_character
    return RedirectResponse("/", status_code=303)

@app.post("/set_points")
def set_points(points: int = Form(...)):
    # Deprecated - kept for reference but redirects to home which will further redirect to edit_character
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

@app.post("/api/calculate_points")
async def calculate_points(request: Request):
    """API endpoint to calculate character points based on traits, abilities, and skills."""
    try:
        form_data = await request.form()
        
        # Get homebrew setting from the request
        homebrew_enabled = form_data.get('homebrew_enabled', 'false').lower() == 'true'
        
        # Get traits and abilities
        from app.traits_api import list_traits
        from app.abilities_api import list_abilities
        trait_costs = {t['name']: t['cost'] for t in list_traits()}
        ability_costs = {a['name']: a['cost'] for a in list_abilities()}
        
        traits_str = form_data.get('traits', '')
        abilities_str = form_data.get('abilities', '')
        
        # Process traits and abilities
        trait_list = [t.strip() for t in traits_str.split(',') if t.strip()]
        ability_list = [a.strip() for a in abilities_str.split(',') if a.strip()]
        
        # Base points cost - same regardless of homebrew setting
        points = 10
        
        # Add costs for traits and abilities
        for t in trait_list:
            points += trait_costs.get(t, 0)
                
        for a in ability_list:
            points += ability_costs.get(a, 0)
        
        # Get skill values, calculate costs
        skill_point_cost = 10  # Each skill level above 1 costs 10 points
        
        # Get skills and calculate their costs
        try:
            agility = max(1, int(form_data.get('agility', 1)))
            shooting = max(1, int(form_data.get('shooting', 1)))
            fighting = max(1, int(form_data.get('fighting', 1)))
            psyche = max(1, int(form_data.get('psyche', 1)))
            awareness = max(1, int(form_data.get('awareness', 1)))
            
            # Get hit-points and calculate cost
            hit_points = int(form_data.get('hit_points', 20))  # Default is 20
            hit_points_change = hit_points - 20  # Calculate change from default
            
            # Calculate cost: +/- 10 points for every 2 hit-points
            hit_points_cost = (hit_points_change // 2) * 10
            
            # Get speed value - default is 10
            speed = int(form_data.get('speed', 10))
            
            # For non-homebrew mode, speed is always 10 and has no cost
            speed_cost = 0
            if homebrew_enabled and speed != 10:
                # In homebrew mode, speed costs can be calculated (10 points per point of speed)
                speed_cost = (speed - 10) * 10
            
            # Enforce maximum skill value of 10 when homebrew is off
            if not homebrew_enabled:
                agility = min(10, agility)
                shooting = min(10, shooting)
                fighting = min(10, fighting)
                psyche = min(10, psyche)
                awareness = min(10, awareness)
            
            # Calculate skill costs
            points += (agility - 1) * skill_point_cost
            points += (shooting - 1) * skill_point_cost
            points += (fighting - 1) * skill_point_cost
            points += (psyche - 1) * skill_point_cost
            points += (awareness - 1) * skill_point_cost
            
            # Add hit-points cost
            points += hit_points_cost
            
            # Add speed cost (only applies in homebrew mode)
            points += speed_cost
            
            # Calculate weapon costs
            weapon_cost = 0
            weapons_input = form_data.get('weapons', '')
            if weapons_input:
                # Split the weapons string into a list of weapon names
                weapon_names = [w.strip() for w in weapons_input.split(',') if w.strip()]
                
                # Import the weapons API functions
                from app.weapons_api import get_weapon
                
                # Look up each weapon and add its cost
                for weapon_name in weapon_names:
                    weapon = get_weapon(weapon_name)
                    if weapon:
                        weapon_cost += weapon.get('cost', 0)
                    else:
                        print(f"Warning: Weapon '{weapon_name}' not found in database")
            
            # Add weapon costs to total points
            points += weapon_cost
            
            # Debug output
            print(f"API Points calculation: homebrew={homebrew_enabled}, skills=[{agility},{shooting},{fighting},{psyche},{awareness}], hit_points={hit_points}, hit_points_cost={hit_points_cost}, speed={speed}, speed_cost={speed_cost}, weapons_cost={weapon_cost}, total_points={points}")
            
            return {"points": points, "success": True}
        except Exception as e:
            print(f"Error calculating skill costs: {e}")
            return {"error": f"Error calculating skill costs: {str(e)}", "success": False}
    except Exception as e:
        print(f"Error in calculate_points API: {e}")
        return {"error": str(e), "success": False}

@app.get("/warbands", response_class=HTMLResponse)
def warbands(request: Request):
    warbands = []
    for d in os.listdir(WARBANDS_DIR):
        if os.path.isdir(os.path.join(WARBANDS_DIR, d)):
            warband_info = {"name": d, "homebrew_enabled": False}
            
            # Check if warband has a config file
            config_path = os.path.join(WARBANDS_DIR, d, "warband_config.json")
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r") as f:
                        config = json.load(f)
                        warband_info["homebrew_enabled"] = config.get("homebrew_enabled", False)
                except:
                    # If there's an error reading the config, use default values
                    pass
            
            warbands.append(warband_info)
            
    return templates.TemplateResponse("warbands.html", {"request": request, "warbands": warbands})

@app.post("/create_warband")
def create_warband(warband_name: str = Form(...), homebrew_enabled: str = Form(None)):
    path = os.path.join(WARBANDS_DIR, warband_name)
    os.makedirs(path, exist_ok=True)
    
    # Print debug info
    print(f"Create warband - Received homebrew_enabled: '{homebrew_enabled}', type: {type(homebrew_enabled)}")
    
    # Save the homebrew setting in a config file
    # The checkbox sends "1" when checked, None when unchecked
    homebrew_value = homebrew_enabled == "1"
    print(f"Create warband - Converted homebrew_value: {homebrew_value}")
    
    config = {
        "homebrew_enabled": homebrew_value,
        "created_at": str(datetime.datetime.now())
    }
    
    with open(os.path.join(path, "warband_config.json"), "w") as f:
        json.dump(config, f)
    
    # Set the new warband as the selected warband in cookie
    response = RedirectResponse("/warbands", status_code=303)
    response.set_cookie(key="warband", value=warband_name)
    return response


def _safe_cookie_key(warband):
    # Only allow alphanum and underscores in cookie keys
    return "warband_points_" + "".join(c if c.isalnum() else "_" for c in warband)

# Add a route to select a warband
@app.get("/select_warband/{warband}")
def select_warband(request: Request, warband: str):
    # Set the warband cookie and redirect to the warband page
    response = RedirectResponse(f"/warband/{warband}", status_code=303)
    response.set_cookie(key="warband", value=warband)
    return response

@app.get("/warband/{warband}", response_class=HTMLResponse)
def warband_dashboard(request: Request, warband: str):
    wb_path = os.path.join(WARBANDS_DIR, warband)
    chars = []
    vehicles = []
    total_points_spent = 0
    homebrew_enabled = False
    
    if os.path.exists(wb_path):
        # Check if warband has a config file
        config_path = os.path.join(wb_path, "warband_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                    # Convert to boolean to handle string values
                    homebrew_enabled_value = config.get("homebrew_enabled", False)
                    if isinstance(homebrew_enabled_value, str):
                        homebrew_enabled = homebrew_enabled_value.lower() == "true"
                    else:
                        homebrew_enabled = bool(homebrew_enabled_value)
                    # Print debug info
                    print(f"Warband dashboard - Read homebrew_enabled from warband config: {homebrew_enabled}")
            except Exception as e:
                # If there's an error reading the config, try global config
                print(f"Error reading warband config: {e}")
                global_config = get_global_config()
                homebrew_enabled = global_config.get("homebrew_enabled", False)
                print(f"Warband dashboard - Using global homebrew_enabled: {homebrew_enabled}")
        else:
            # If no warband config exists, try global config
            global_config = get_global_config()
            homebrew_enabled = global_config.get("homebrew_enabled", False)
            print(f"Warband dashboard - Using global homebrew_enabled: {homebrew_enabled}")
                
        chars = [f[:-5] for f in os.listdir(wb_path) if f.endswith('.json') and not f.startswith('vehicle_') and f != "warband_config.json"]
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
    return templates.TemplateResponse("warband_dashboard.html", {
        "request": request, 
        "warband": warband, 
        "characters": chars, 
        "vehicles": vehicles, 
        "warband_points": warband_points, 
        "total_points_spent": total_points_spent,
        "homebrew_enabled": homebrew_enabled
    })

# Set warband points limit
@app.post("/set_warband_points/{warband}")
def set_warband_points(request: Request, warband: str, points: int = Form(...)):
    cookie_key = _safe_cookie_key(warband)
    response = RedirectResponse(f"/warband/{warband}", status_code=303)
    response.set_cookie(key=cookie_key, value=str(points))
    return response

# Toggle homebrew setting
@app.post("/toggle_homebrew/{warband}")
def toggle_homebrew(request: Request, warband: str, homebrew_enabled: str = Form(None)):
    wb_path = os.path.join(WARBANDS_DIR, warband)
    config_path = os.path.join(wb_path, "warband_config.json")
    
    # Print debug info
    print(f"Received homebrew_enabled: '{homebrew_enabled}', type: {type(homebrew_enabled)}")
    
    # Create or update the config file
    # Convert the form value to a boolean
    # Form checkbox sends "1" when checked, None when unchecked
    homebrew_value = homebrew_enabled == "1"
    print(f"Converted homebrew_value: {homebrew_value}")
    
    config = {"homebrew_enabled": homebrew_value}
    
    # If the config file exists, read existing settings and update only the homebrew setting
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                existing_config = json.load(f)
                # Preserve other settings
                for key, value in existing_config.items():
                    if key != "homebrew_enabled":
                        config[key] = value
        except:
            # If there's an error reading the config, just use the new config
            pass
    
    # Save the updated config
    with open(config_path, "w") as f:
        json.dump(config, f)
    
    return RedirectResponse(f"/warband/{warband}", status_code=303)

@app.post("/add_character")
def add_character(request: Request, char_name: str = Form(...)):
    warband = request.cookies.get("warband")
    if not warband:
        return RedirectResponse("/warbands", status_code=303)
    wb_path = os.path.join(WARBANDS_DIR, warband)
    os.makedirs(wb_path, exist_ok=True)
    char_file = os.path.join(wb_path, f"{char_name}.json")
    # Complete character template with all required fields
    char_data = {
        'Name': char_name,
        'Points': 10,
        'Skills': {'Agility': 1, 'Fighting': 1, 'Shooting': 1, 'Awareness': 1, 'Psyche': 1},
        'Speed': 10,
        'Hit-points': 20,
        'Traits': [],
        'Abilities': [],
        'Equipment': [],
        'Weapons': [],
        'Notes': '',
        'Backstory': '',
        'Injuries': '',
        'CampaignPoints': ''
    }
    with open(char_file, 'w') as f:
        json.dump(char_data, f, indent=2)
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



# --- Character Edit Routes ---
@app.get("/edit_character/{warband}/{char_name}", response_class=HTMLResponse)
def edit_character_get(request: Request, warband: str, char_name: str):
    wb_path = os.path.join(WARBANDS_DIR, warband)
    char_file = os.path.join(wb_path, f"{char_name}.json")
    
    # Check if warband has homebrew enabled
    homebrew_enabled = False
    config_path = os.path.join(wb_path, "warband_config.json")
    
    # First try to get homebrew setting from warband config
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                # Convert to boolean to handle string values
                homebrew_enabled_value = config.get("homebrew_enabled", False)
                if isinstance(homebrew_enabled_value, str):
                    homebrew_enabled = homebrew_enabled_value.lower() == "true"
                else:
                    homebrew_enabled = bool(homebrew_enabled_value)
                # Print debug info
                print(f"Edit character get - Read homebrew_enabled from warband config: {homebrew_enabled}")
        except Exception as e:
            # If there's an error reading the config, try global config
            print(f"Error reading warband config: {e}")
            global_config = get_global_config()
            homebrew_enabled = global_config.get("homebrew_enabled", False)
            print(f"Edit character get - Using global homebrew_enabled: {homebrew_enabled}")
    else:
        # If no warband config exists, try global config
        global_config = get_global_config()
        homebrew_enabled = global_config.get("homebrew_enabled", False)
        print(f"Edit character get - Using global homebrew_enabled: {homebrew_enabled}")
    
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
        {
            "request": request, 
            "warband": warband, 
            "character": character, 
            "traits": traits, 
            "abilities": abilities, 
            "warband_points": warband_points, 
            "mod_skills": mod_skills,
            "homebrew_enabled": homebrew_enabled
        }
    )

@app.post("/edit_character/{warband}/{char_name}")
async def edit_character_post(request: Request, warband: str, char_name: str):
    form = await request.form()
    wb_path = os.path.join(WARBANDS_DIR, warband)
    char_file = os.path.join(wb_path, f"{char_name}.json")
    
    # Check if warband has homebrew enabled
    homebrew_enabled = False
    config_path = os.path.join(wb_path, "warband_config.json")
    
    # First try to get homebrew setting from warband config
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                # Convert to boolean to handle string values
                homebrew_enabled_value = config.get("homebrew_enabled", False)
                if isinstance(homebrew_enabled_value, str):
                    homebrew_enabled = homebrew_enabled_value.lower() == "true"
                else:
                    homebrew_enabled = bool(homebrew_enabled_value)
                # Print debug info
                print(f"Edit character post - Read homebrew_enabled from warband config: {homebrew_enabled}")
        except Exception as e:
            # If there's an error reading the config, try global config
            print(f"Error reading warband config: {e}")
            global_config = get_global_config()
            homebrew_enabled = global_config.get("homebrew_enabled", False)
            print(f"Edit character post - Using global homebrew_enabled: {homebrew_enabled}")
    else:
        # If no warband config exists, try global config
        global_config = get_global_config()
        homebrew_enabled = global_config.get("homebrew_enabled", False)
        print(f"Edit character post - Using global homebrew_enabled: {homebrew_enabled}")
    
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
    
    # Debug
    print(f"Received Traits: '{traits}'")
    print(f"Received Abilities: '{abilities}'")
    
    # Process lists with consistent delimiter handling
    trait_list = [t.strip() for t in traits.split(',') if t.strip()]
    ability_list = [a.strip() for a in abilities.split(',') if a.strip()]
    equipment_list = [e.strip() for e in equipment.split(',') if e.strip()]
    
    # Debug
    print(f"Processed trait_list: {trait_list}")
    print(f"Processed ability_list: {ability_list}")
    
    # Remove duplicates
    trait_list = list(dict.fromkeys(trait_list))
    ability_list = list(dict.fromkeys(ability_list))
    
    # Base points cost - same regardless of homebrew setting
    points = 10
    
    # Add costs for traits and abilities
    for t in trait_list:
        points += trait_costs.get(t, 0)
            
    for a in ability_list:
        points += ability_costs.get(a, 0)
    
    # Get skill values from the form, ensuring minimum value of 1
    try:
        agility = max(1, int(form.get('Agility', character['Skills']['Agility'])))
    except (ValueError, TypeError):
        agility = 1
        
    try:
        shooting = max(1, int(form.get('Shooting', character['Skills']['Shooting'])))
    except (ValueError, TypeError):
        shooting = 1
        
    try:
        fighting = max(1, int(form.get('Fighting', character['Skills']['Fighting'])))
    except (ValueError, TypeError):
        fighting = 1
        
    try:
        psyche = max(1, int(form.get('Psyche', character['Skills']['Psyche'])))
    except (ValueError, TypeError):
        psyche = 1
        
    try:
        awareness = max(1, int(form.get('Awareness', character['Skills']['Awareness'])))
    except (ValueError, TypeError):
        awareness = 1
    
    # Enforce maximum skill value of 10 when homebrew is off
    if not homebrew_enabled:
        agility = min(10, agility)
        shooting = min(10, shooting)
        fighting = min(10, fighting)
        psyche = min(10, psyche)
        awareness = min(10, awareness)
    
    # Calculate skill costs (each skill starts at 1, costs 10 points per level above 1)
    skill_point_cost = 10
    
    points += (agility - 1) * skill_point_cost
    points += (shooting - 1) * skill_point_cost
    points += (fighting - 1) * skill_point_cost
    points += (psyche - 1) * skill_point_cost
    points += (awareness - 1) * skill_point_cost
    
    # Calculate hit-points cost (+/- 10 points for every 2 hit-points)
    try:
        hit_points = int(form.get('Hitpoints', 20))
        # Calculate difference from default 20 hit-points
        hit_points_change = hit_points - 20
        # Calculate cost (10 points per 2 hit-points)
        hit_points_cost = (hit_points_change // 2) * 10
        points += hit_points_cost
    except (ValueError, TypeError):
        hit_points = 20  # Default to 20 if invalid
    
    # Calculate weapon costs
    weapon_cost = 0
    weapons = form.get('Weapons', '')
    weapon_list = [w.strip() for w in weapons.split(',') if w.strip()]
    
    # Import weapons API functions
    from app.weapons_api import get_weapon
    
    # Look up each weapon and add its cost
    for weapon_name in weapon_list:
        weapon = get_weapon(weapon_name)
        if weapon:
            weapon_cost += weapon.get('cost', 0)
        else:
            print(f"Warning: Weapon '{weapon_name}' not found in database")
    
    # Add weapon costs to total points
    points += weapon_cost
    print(f"Weapon costs: {weapon_cost}")
    
    # Handle Speed
    try:
        # Get speed from form
        speed = int(form.get('Speed', 10))
        
        # If not in homebrew mode, speed is always 10 (default)
        if not homebrew_enabled:
            speed = 10
        else:
            # In homebrew mode, calculate speed cost (10 points per point of speed difference)
            speed_cost = (speed - 10) * 10
            points += speed_cost
    except (ValueError, TypeError):
        speed = 10  # Default to 10 if invalid
    
    # Update character with new values
    character['Points'] = points
    character['Skills']['Agility'] = agility
    character['Skills']['Shooting'] = shooting
    character['Skills']['Fighting'] = fighting
    character['Skills']['Psyche'] = psyche
    character['Skills']['Awareness'] = awareness
    character['Speed'] = speed
    character['Hit-points'] = hit_points
    
    # Process weapons
    weapons = form.get('Weapons', '')
    weapon_list = [w.strip() for w in weapons.split(',') if w.strip()]
    
    # Debug
    print(f"Final trait_list before save: {trait_list}")
    print(f"Final ability_list before save: {ability_list}")
    print(f"Final weapon_list before save: {weapon_list}, total weapon cost: {weapon_cost}")
    
    # Update collections using the processed lists (ensures removed items stay removed)
    character['Traits'] = trait_list
    character['Abilities'] = ability_list
    character['Equipment'] = equipment_list
    character['Weapons'] = weapon_list
    
    # Debug
    print(f"Character after update: Traits={character['Traits']}, Abilities={character['Abilities']}, Weapons={character['Weapons']}")
    
    # Save notes/background and new fields
    character['Notes'] = form.get('Notes', character.get('Notes', ''))
    character['Backstory'] = form.get('Backstory', character.get('Backstory', ''))
    character['Injuries'] = form.get('Injuries', character.get('Injuries', ''))
    character['CampaignPoints'] = form.get('CampaignPoints', character.get('CampaignPoints', ''))
    
    # Save back to file (rename if name changed)
    new_name = character['Name']
    new_char_file = os.path.join(wb_path, f"{new_name}.json")
    
    # Make sure traits and abilities are properly reset when empty
    if not trait_list:
        character['Traits'] = []
    if not ability_list:
        character['Abilities'] = []
    
    with open(new_char_file, "w") as f:
        json.dump(character, f, indent=2)
    
    print(f"Saved character to {new_char_file}")
    
    if new_char_file != char_file and os.path.exists(char_file):
        os.remove(char_file)
        print(f"Removed old character file {char_file}")
        
    # Check if this is an AJAX request for auto-save
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        # For AJAX requests, return a success message instead of redirecting
        from fastapi.responses import JSONResponse
        return JSONResponse({"status": "success", "message": "Character saved"})
    else:
        # For normal form submissions, redirect as before
        return RedirectResponse(f"/warband/{warband}", status_code=303)

# --- Weapon Routes ---
@app.get("/weapons/{warband}/{character_name}", response_class=HTMLResponse)
def weapons_page(request: Request, warband: str, character_name: str):
    """Display the weapons page for selecting weapons to equip."""
    from app.weapons_api import list_weapons, get_weapon_types, get_special_rules
    
    # Get weapons data
    weapons = list_weapons()
    weapon_types = get_weapon_types()
    special_rules = get_special_rules()
    
    return templates.TemplateResponse(
        "weapons.html",
        {
            "request": request,
            "warband": warband,
            "character_name": character_name,
            "weapons": weapons,
            "weapon_types": weapon_types,
            "special_rules": special_rules
        }
    )

@app.get("/weapon_rules/{warband}", response_class=HTMLResponse)
def weapon_rules(request: Request, warband: str):
    """Display the weapon special rules reference page."""
    return templates.TemplateResponse(
        "weapon_rules.html",
        {
            "request": request,
            "warband": warband
        }
    )

@app.get("/weapon_cost_table/{warband}", response_class=HTMLResponse)
def weapon_cost_table(request: Request, warband: str):
    """Display the weapon special rules cost table."""
    return templates.TemplateResponse(
        "weapon_cost_table.html",
        {
            "request": request,
            "warband": warband
        }
    )

@app.post("/add_weapon/{warband}/{character_name}")
def add_weapon(request: Request, warband: str, character_name: str, weapon_name: str = Form(...)):
    """Add a weapon to a character."""
    wb_path = os.path.join(WARBANDS_DIR, warband)
    char_file = os.path.join(wb_path, f"{character_name}.json")
    
    if not os.path.exists(char_file):
        return RedirectResponse(f"/warband/{warband}", status_code=303)
    
    with open(char_file, "r") as f:
        character = json.load(f)
    
    # Initialize weapons list if it doesn't exist
    if 'Weapons' not in character:
        character['Weapons'] = []
    
    # Add the weapon if it's not already in the list
    if weapon_name not in character['Weapons']:
        character['Weapons'].append(weapon_name)
    
    # Save the updated character
    with open(char_file, "w") as f:
        json.dump(character, f, indent=2)
    
    return RedirectResponse(f"/edit_character/{warband}/{character_name}", status_code=303)

@app.post("/remove_weapon/{warband}/{character_name}")
def remove_weapon(request: Request, warband: str, character_name: str, weapon_name: str = Form(...)):
    """Remove a weapon from a character."""
    wb_path = os.path.join(WARBANDS_DIR, warband)
    char_file = os.path.join(wb_path, f"{character_name}.json")
    
    if not os.path.exists(char_file):
        return RedirectResponse(f"/warband/{warband}", status_code=303)
    
    with open(char_file, "r") as f:
        character = json.load(f)
    
    # Remove the weapon if it's in the list
    if 'Weapons' in character and weapon_name in character['Weapons']:
        character['Weapons'].remove(weapon_name)
    
    # Save the updated character
    with open(char_file, "w") as f:
        json.dump(character, f, indent=2)
    
    return RedirectResponse(f"/edit_character/{warband}/{character_name}", status_code=303)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

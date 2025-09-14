from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

from traits_api import list_traits, get_trait
from abilities_api import list_abilities, get_ability
from arcana_api import list_arcana

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

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


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

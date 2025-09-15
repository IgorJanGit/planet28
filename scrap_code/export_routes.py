# Export routes that were removed from main.py

# Export route for single character
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

# Export route for entire warband
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
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import pickle


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# parametrages pour préciser que le template html est dans le directory template et
#le template css est dans le directory static
templates = Jinja2Templates(directory="../templates")
app.mount("/static", StaticFiles(directory="../static"), name="static")


# Ajout de cette méthode pour gérer l'erreur d'accessibilité 'access-control-allow-origin'
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {"page": "ce ci est importé dans le script html par data.page"}
    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": data
    })


# @app.get("/page/{page_name}", response_class=HTMLResponse)
# async def page(request: Request, page_name: str):
#     data = {"page": page_name}
#     return templates.TemplateResponse("index.html", {
#         "request": request,
#         "data": data
#     })


@app.post("/property",  response_class=HTMLResponse)
async def property_dict(request: Request,
                        nom: str = Form(...),
                        prenom: str = Form(...),
                        email: str = Form(...),
                        adress: str = Form(...),
                        commune: str = Form(...),
                        code_postal: str = Form(...),
                        nb_pieces_principales: float = Form(...),
                        surface_reelle_bati: float = Form(...),
                        surface_terrain: float = Form(...),
                        Dependance: bool= Form(...)):
    # check à faire si cela doit rentrer sous forme de liste ?
    property = {
       # 'nom': [nom],
       # 'prenom ': [prenom],
       # 'email': [email],
        'adress': [adress],
        'commune': [commune],
        'code_postal': [code_postal],
        'nb_pieces_principales': [nb_pieces_principales],
        'surface_reelle_bati': [surface_reelle_bati],
        'surface_terrain': [surface_terrain],
        'Dependance': [Dependance]
    }
    X = pd.DataFrame(property)
    # enrichissement coordonnées
    # enrichissement IRIS
    # enrichissement stats
    # appel modele
    ## le chargement du modele doit être fait depuis la class ML !! et le stockage du modele doit être fait dans le package
    filename="../notebooks/house_dep_model_aggregations_logement_act.sav"
    loaded_model = pickle.load(open(filename, 'rb'))
    pred = loaded_model.predict(X)

    # return  {'result': X}
    return templates.TemplateResponse("form_response.html",
                                      {"request": request, "data": X})

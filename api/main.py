from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import pandas as pd
from retraitement import prepare_received_data
from data import loading_data_in_db
from enrichissement import external_api_calls
import pickle



from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# parametrages pour préciser que le template html est dans le directory template et
#le template css est dans le directory static
templates = Jinja2Templates(directory="../templates")
# mount directory under /static path. # Access to static files in your html need to use static prefix
app.mount("/static", StaticFiles(directory="../static"), name="static")


# Ajout de cette méthode pour gérer l'erreur d'accessibilité 'access-control-allow-origin'
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def get_root():
    return {'message': 'Welcome to the real estate evaluation app'}

@app.get("/property", response_class=HTMLResponse)
async def home(request: Request):
    info = {"page": "ceci est importé dans le script html par data.page"}
    return templates.TemplateResponse("index.html", {
        "request": request
    #       ,"data": info
    })

## attention à bien ajouter l'ption name qui matchent les noms ci dessous dans html l'input des forms
# champs optionnels en ajoutant None
@app.post("/property")
async def post_properties_feature(request: Request,
                        nom: str = Form(...),
                        prenom: str = Form(...),
                        email: str = Form(...),
                        addresse: str = Form(...),
                        complement: str = Form(None),
                        lieu : str = Form(...),
                        commune: str = Form(...),
                        code_postal: str = Form(...),
                        nb_pieces_principales: float = Form(...),
                        surface_reelle_bati: float = Form(...),
                        surface_terrain: float = Form(...),
                        Dependance: bool = Form(...)):


    df= external_api_calls(addresse, complement,lieu, commune,code_postal,
                     nb_pieces_principales,surface_reelle_bati,
                     surface_terrain,Dependance).call_api_addresse().call_api_pyris()

    df = prepare_received_data(df).dependance().columns_featuring_act(
    ).columns_featuring_log().feature_generation()

    filename = 'house_dep_model_aggregations_logement_act.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    result=loaded_model.predict(df)
    result= int(round(result[0]))

    loading_data_in_db(df, 'house_pred_database',
                       'demands',result).load_df_db()

    return templates.TemplateResponse("index.html",context={'request': request, 'result': result,
     'surface':surface_reelle_bati, 'commune': commune
    })

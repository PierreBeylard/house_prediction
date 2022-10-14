from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import pandas as pd
from .retraitement import PrepareReceivedData
from .data import LoadingDataInDb
from .enrichissement import ExternalApiCalls, FraisCalculation
import pickle


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# parametrages pour préciser que le template html est dans le directory template et
#le template css est dans le directory static
templates = Jinja2Templates(directory="./templates")
# mount directory under /static path. # Access to static files in your html need to use static prefix
app.mount("/static", StaticFiles(directory="./static"), name="static")


# Ajout de cette méthode pour gérer l'erreur d'accessibilité 'access-control-allow-origin'
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', response_class=HTMLResponse)
async def get_root():
    info = {"page": "ceci est importé dans le script html par data.page"}
    return templates.TemplateResponse(
        "cover.html", context={"request":info})


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
                        Dependance: bool = Form(...),
                        neuf : str = Form(...),
                        terrain : str = Form(...)):


    df = ExternalApiCalls(addresse, complement, lieu, commune, code_postal,
                          nb_pieces_principales, surface_reelle_bati,
                          surface_terrain, Dependance,
                          terrain).call_api_addresse().call_api_pyris()
    iris = df.at[0, 'IRIS']
    df = PrepareReceivedData(df).dep_and_terrain().columns_featuring_act(
    ).columns_featuring_log().feature_generation()
    #test_19_08  house_dep_model_aggregations_logement_act
    # 'test_21_08_linear_corrected.sav'
    filename = "test_21_08_linear_corrected_minmax_20p.sav"
    loaded_model = pickle.load(open(filename, 'rb'))
    result=loaded_model.predict(df)
    result= int(round(result[0]))
    low_result = int(round(result - (result*10/100)))
    high_result = int(round(result + (result*10/100)))

    LoadingDataInDb(df, 'production', 'demands',iris,
                    result).load_df_db_psql()

    frais_notaire_low, frais_notaire, frais_notaire_high = FraisCalculation(
        low_result, result, high_result, neuf).frais_notaires()
    frais_agence_low, frais_agence, frais_agence_high = FraisCalculation(
        low_result, result, high_result, neuf).frais_agence()

    return templates.TemplateResponse("index.html",
                                      context={
                                          'request': request,
                                          'result': result,
                                          'surface': surface_reelle_bati,
                                          'pieces': int(round(nb_pieces_principales)),
                                          'commune': commune,
                                          'low_result': low_result,
                                          'high_result': high_result,
                                          'frais_notaire_low':
                                          frais_notaire_low,
                                          'frais_notaire': frais_notaire,
                                          'frais_notaire_high':
                                          frais_notaire_high,
                                          'frais_agence_low':frais_agence_low,
                                           'frais_agence':frais_agence,
                                            'frais_agence_high':frais_agence_high
                                      })

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import pandas as pd
from sqlalchemy import create_engine
from retraitement import prepare_received_data
import pickle



from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# parametrages pour préciser que le template html est dans le directory template et
#le template css est dans le directory static
templates = Jinja2Templates(directory="../templates")
# mount directory under /static path. # Access to static files in your html need to use static prefix
app.mount("/static", StaticFiles(directory="../static"), name="static")
engine = create_engine('sqlite:///../data/house_pred_database.sqlite',
                                echo=True)

# Ajout de cette méthode pour gérer l'erreur d'accessibilité 'access-control-allow-origin'
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
                        commune: str = Form(...),
                        code_postal: str = Form(...),
                        nb_pieces_principales: float = Form(...),
                        surface_reelle_bati: float = Form(...),
                        surface_terrain: float = Form(...),
                        Dependance: bool = Form(...)):

    addresse_for_enrichment = (addresse, str(complement), commune)
    addresse_for_enrichment = "+".join(addresse_for_enrichment).replace(
        " ", "+").replace("None+", "")
    addresse_for_enrichment =  addresse_for_enrichment+ '&postcode='+code_postal
    addresse_api_url ="https://api-adresse.data.gouv.fr/search/?q="
    result = requests.get(
        f'{addresse_api_url}{addresse_for_enrichment}').json()['features'][0]
    try :
        long = result['geometry']['coordinates'][0]
        lat = result['geometry']['coordinates'][1]
        clean_code_commune = result['properties']['citycode']
        clean_code_departement = result['properties']['context'].split(',')[0]
        type_de_voie = result['properties']['street'].split(' ')[0]
        code_postal = result['properties']['postcode']
    except :
        long = 'not found'
        lat = 'not found'
    coordinates =(str(lat),str(long))
    coordinates = "&lon=".join(coordinates)
    pyris_api_url= "https://pyris.datajazz.io/api/coords?geojson=false&lat="
    try :
        IRIS=requests.get(f'{pyris_api_url}{coordinates}').json()['complete_code']
    except  :
        IRIS='not found'
    print(IRIS)
    property_dict = {
        'type_de_voie': [type_de_voie],
        'clean_code_departement': [clean_code_departement],
        'clean_code_commune': [clean_code_commune],
        'code_postal': [code_postal],
        'surface_terrain': [surface_terrain],
        'surface_reelle_bati': [surface_reelle_bati],
        'nb_pieces_principales': [nb_pieces_principales],
        'Dependance': [Dependance],
        'main_type_terrain': ['']
    }
    df = pd.DataFrame(property_dict)
    df['IRIS']= IRIS
    variables_to_keep=["IRIS", "LAB_IRIS","P18_LOG", "P18_RP", "P18_RSECOCC", "P18_LOGVAC", "P18_MAISON",
     "P18_APPART","P18_RP_1P", "P18_RP_2P", "P18_RP_3P", "P18_RP_4P", "P18_RP_5PP","P18_RP_M30M2",
      "P18_RP_3040M2", "P18_RP_4060M2", "P18_RP_6080M2", "P18_RP_80100M2", "P18_RP_100120M2",
       "P18_RP_120M2P","P18_RP_GARL","P18_RP_PROP","P18_RP_LOC", "P18_RP_LOCHLMV","P18_RP_GRAT",
       "P18_MEN_ANEM0002", "P18_MEN_ANEM0204", "P18_MEN_ANEM0509", "P18_MEN_ANEM10P"]
    df_stat =pd.read_sql_query(f'SELECT * FROM logements_stats WHERE IRIS= {IRIS}', con=engine)
    df_stat=df_stat[variables_to_keep]
    df= pd.concat([df,df_stat],axis=1)
    df_stat = pd.read_sql_query(
        f'SELECT * FROM activites_stat WHERE IRIS= {IRIS}', con=engine)
    variables_to_keep = [
        "IRIS", "P18_POP1564", "P18_POP1524", "P18_POP2554", "P18_POP5564",
        "P18_ACT1564", "P18_ACTOCC1564", "P18_CHOM1564", "C18_ACT1564",
        "C18_ACT1564_CS1", "C18_ACT1564_CS3", "C18_ACT1564_CS2",
        "C18_ACT1564_CS4", "C18_ACTOCC1564", "C18_ACTOCC1564_CS1",
        "C18_ACTOCC1564_CS2", "C18_ACTOCC1564_CS3", "C18_ACTOCC1564_CS4",
        "P18_ACTOCC15P_ILT1", "C18_ACTOCC15P", "C18_ACTOCC15P_PAS",
        "C18_ACTOCC15P_MAR", "C18_ACTOCC15P_VELO", "C18_ACTOCC15P_2ROUESMOT",
        "C18_ACTOCC15P_VOIT", "C18_ACTOCC15P_TCOM"
    ]
    df_stat=df_stat[variables_to_keep]
    df= pd.concat([df,df_stat],axis=1)
    df = prepare_received_data(
        df).columns_featuring_act().columns_featuring_log().feature_generation()
    print(df.dtypes)
    filename = 'house_dep_model_aggregations_logement_act.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    result=loaded_model.predict(df)
    print(df)
    return templates.TemplateResponse("index.html", {
        "request": request
    })

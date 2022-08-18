import requests
import pandas as pd
from sqlalchemy import create_engine

class external_api_calls :
    """external calls to :
    api address gouv for geo coordinates, uniformised street, departement & city code
    api pyris in order to obtain IRIS from coordinates """

    def __init__ (self, addresse, complement, commune,code_postal,
                     nb_pieces_principales,surface_reelle_bati,surface_terrain,Dependance):
        self.addresse = addresse
        self.complement = complement
        self.commune = commune
        self.code_postal = code_postal
        self.nb_pieces_principales = nb_pieces_principales
        self.surface_reelle_bati = surface_reelle_bati
        self.surface_terrain = surface_terrain
        self.Dependance = Dependance

    def call_api_addresse (self) :
        addresse_for_enrichment = (self.addresse, str(self.complement), self.commune)

        addresse_for_enrichment = "+".join(addresse_for_enrichment).replace(
            " ", "+").replace("None+", "")
        addresse_for_enrichment = addresse_for_enrichment + '&postcode=' + self.code_postal
        addresse_api_url = "https://api-adresse.data.gouv.fr/search/?q="
        result = requests.get(
            f'{addresse_api_url}{addresse_for_enrichment}').json()['features'][0]
        try:
            self.long = result['geometry']['coordinates'][0]
            self.lat = result['geometry']['coordinates'][1]
            self.clean_code_commune = result['properties']['citycode']
            self.clean_code_departement = result['properties']['context'].split(',')[0]
            try :
                self.type_de_voie = result['properties']['street'].split(' ')[0]
            except :
                self.type_de_voie = result['properties']['name'].split(' ')[0]
            self.code_postal = result['properties']['postcode']
        except:
            self.long = 'not found'
            self.lat = 'not found'
        self.coordinates = (str(self.lat), str(self.long))
        self.coordinates = "&lon=".join(self.coordinates)
        return self

    def call_api_pyris (self):
        ## reste à faire -- appel vers d'autres API en fonction de la région Metropole, DOM ...)
        pyris_api_url = "https://pyris.datajazz.io/api/coords?geojson=false&lat="
        try:
            IRIS = requests.get(
                f'{pyris_api_url}{self.coordinates}').json()['complete_code']
        except:
            IRIS = 'not found'
        property_dict = {
            'type_de_voie': [self.type_de_voie],
            'clean_code_departement': [self.clean_code_departement],
            'clean_code_commune': [self.clean_code_commune],
            'code_postal': [self.code_postal],
            'surface_terrain': [self.surface_terrain],
            'surface_reelle_bati': [self.surface_reelle_bati],
            'nb_pieces_principales': [self.nb_pieces_principales],
            'Dependance': [self.Dependance],
            'main_type_terrain': ['']
        }
        self.df = pd.DataFrame(property_dict)
        self.df['IRIS'] = IRIS
        variables_to_keep = [
            "IRIS", "LAB_IRIS", "P18_LOG", "P18_RP", "P18_RSECOCC", "P18_LOGVAC",
            "P18_MAISON", "P18_APPART", "P18_RP_1P", "P18_RP_2P", "P18_RP_3P",
            "P18_RP_4P", "P18_RP_5PP", "P18_RP_M30M2", "P18_RP_3040M2",
            "P18_RP_4060M2", "P18_RP_6080M2", "P18_RP_80100M2", "P18_RP_100120M2",
            "P18_RP_120M2P", "P18_RP_GARL", "P18_RP_PROP", "P18_RP_LOC",
            "P18_RP_LOCHLMV", "P18_RP_GRAT", "P18_MEN_ANEM0002",
            "P18_MEN_ANEM0204", "P18_MEN_ANEM0509", "P18_MEN_ANEM10P"
        ]
        engine = create_engine('sqlite:///../data/house_pred_database.sqlite',
                               echo=True)
        df_stat = pd.read_sql_query(
            f'SELECT * FROM logements_stats WHERE IRIS= {IRIS}', con=engine)
        df_stat = df_stat[variables_to_keep]
        self.df = pd.concat([self.df, df_stat], axis=1)
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
        df_stat = df_stat[variables_to_keep]
        self.df = pd.concat([self.df, df_stat], axis=1)
        return self.df

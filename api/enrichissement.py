import requests
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ.get('DB_STRING')
DB_NAME = os.environ.get('DB_NAME')


class ExternalApiCalls :
    """external calls to :
    api address gouv for geo coordinates, uniformised street, departement & city code
    api pyris in order to obtain IRIS from coordinates
    """

    def __init__ (self, addresse, complement, lieu, commune,code_postal,
                     nb_pieces_principales,surface_reelle_bati,surface_terrain,Dependance,terrain):
        self.addresse = addresse
        self.complement = complement
        self.lieu = lieu
        self.commune = commune
        self.code_postal = code_postal
        self.nb_pieces_principales = nb_pieces_principales
        self.surface_reelle_bati = surface_reelle_bati
        self.surface_terrain = surface_terrain
        self.Dependance = Dependance
#        self.type = type
        self.terrain = terrain

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
        if self.lieu == 'France Metropolitaine':
            url = "https://pyris.datajazz.io/api/coords?geojson=false&lat="
            try:
                IRIS = requests.get(
                f'{url}{self.coordinates}').json()['complete_code']
            except:
                IRIS = 'not found'
        elif self.lieu == 'La Guadeloupe':
            url =f"https://regionguadeloupe.opendatasoft.com/api/records/1.0/search/?dataset=iris-millesime-france&q={self.clean_code_commune}&sort=year&facet=com_arm_name"
            try:
                IRIS = requests.get(
                    f'{url}').json()['records'][0]['fields']['iris_code']
            except:
                IRIS = 'not found'
        elif self.lieu == 'La Martinique':
            url = f"https://public.opendatasoft.com/api/records/1.0/search/?dataset=georef-france-iris&q={self.clean_code_commune}&sort=year&facet=com_arm_name"
            try:
                IRIS = requests.get(
                    f'{url}').json()['records'][0]['fields']['iris_code']
            except:
                IRIS = 'not found'
        elif self.lieu == 'La Reunion':
            url = f"https://data.opendatasoft.com/api/records/1.0/search/?dataset=iris-millesime-france%40lareunion&q={self.clean_code_commune}&sort=year&facet=com_arm_name"
            try:
                IRIS = requests.get(
                    f'{url}').json()['records'][0]['fields']['iris_code']
            except:
                IRIS = 'not found'
        # if self.Dependance == True :
        #     self.type = self.type + ' with dependance'
        property_dict = {
            'type_de_voie': [self.type_de_voie],
            'clean_code_departement': [self.clean_code_departement],
            'clean_code_commune': [self.clean_code_commune],
            'code_postal': [self.code_postal],
            'surface_terrain': [self.surface_terrain],
            'surface_reelle_bati': [self.surface_reelle_bati],
            'nb_pieces_principales': [self.nb_pieces_principales],
            'Dependance': [self.Dependance],
#            'multi_locaux_clean' : [self.type],
            'main_type_terrain': [self.terrain]
        }
        self.df = pd.DataFrame(property_dict)
        self.df['IRIS'] = IRIS

        # nouvelle version pour mise en prod :
        # Connection à la base PostgreSQL production
        # enlever le password en dur et le mettre dans un fichier config
        engine = create_engine(f'{DATABASE_URL}{DB_NAME}', echo=False)
        df_stat = pd.read_sql_query(
            f'SELECT * FROM iris_insee WHERE "IRIS" ={IRIS}::TEXT', con=engine)
        variables_to_keep = [ "LAB_IRIS", "P18_LOG", "P18_RP", "P18_RSECOCC",
            "P18_LOGVAC", "P18_MAISON", "P18_APPART", "P18_RP_1P", "P18_RP_2P",
            "P18_RP_3P", "P18_RP_4P", "P18_RP_5PP", "P18_NBPI_RP","P18_RP_M30M2",
            "P18_RP_3040M2", "P18_RP_4060M2", "P18_RP_6080M2",
            "P18_RP_80100M2", "P18_RP_100120M2", "P18_RP_120M2P",
            "P18_RP_GARL", "P18_RP_PROP", "P18_RP_LOC", "P18_RP_LOCHLMV",
            "P18_RP_GRAT", "P18_MEN_ANEM0002", "P18_MEN_ANEM0204",
            "P18_MEN_ANEM0509", "P18_MEN_ANEM10P", "P18_RP_ACHTOT",
            "P18_RP_ACH19", "P18_RP_ACH45", "P18_RP_ACH70",
           "P18_RP_ACH90", "P18_RP_ACH05","P18_RP_ACH15",
            "P18_POP","P18_POP1564",
            "P18_POP1524", "P18_POP2554", "P18_POP5564",
            "P18_ACT1564", "P18_ACTOCC1564", "P18_CHOM1564", "C18_ACT1564",
            "C18_ACT1564_CS1", "C18_ACT1564_CS3", "C18_ACT1564_CS2",
            "C18_ACT1564_CS4","C18_ACT1564_CS5", "C18_ACT1564_CS6", "P18_PMEN",
            "C18_ACTOCC1564", "C18_ACTOCC1564_CS1",
            "C18_ACTOCC1564_CS2", "C18_ACTOCC1564_CS3", "C18_ACTOCC1564_CS4",
            "P18_ACTOCC15P_ILT1", "C18_ACTOCC15P", "C18_ACTOCC15P_PAS",
            "C18_ACTOCC15P_MAR", "C18_ACTOCC15P_VELO", "C18_ACTOCC15P_2ROUESMOT",
            "C18_ACTOCC15P_VOIT", "C18_ACTOCC15P_TCOM"]
        df_stat = df_stat[variables_to_keep]
        self.df = pd.concat([self.df, df_stat], axis=1)
        return self.df

        # Anciene version -connection à sqlite sur chaque table :
        # variables_to_keep = [
        #     "IRIS", "LAB_IRIS", "P18_LOG", "P18_RP", "P18_RSECOCC",
        #     "P18_LOGVAC", "P18_MAISON", "P18_APPART", "P18_RP_1P", "P18_RP_2P",
        #     "P18_RP_3P", "P18_RP_4P", "P18_RP_5PP", "P18_RP_M30M2",
        #     "P18_RP_3040M2", "P18_RP_4060M2", "P18_RP_6080M2",
        #     "P18_RP_80100M2", "P18_RP_100120M2", "P18_RP_120M2P",
        #     "P18_RP_GARL", "P18_RP_PROP", "P18_RP_LOC", "P18_RP_LOCHLMV",
        #     "P18_RP_GRAT", "P18_MEN_ANEM0002", "P18_MEN_ANEM0204",
        #     "P18_MEN_ANEM0509", "P18_MEN_ANEM10P"
        # ]
        # engine = create_engine('sqlite:///../data/house_pred_database.sqlite'
        #                        , echo=True)
        # df_stat = pd.read_sql_query(
        #     f'SELECT * FROM logements_stats WHERE IRIS= {IRIS}', con=engine)
        # df_stat = df_stat[variables_to_keep]
        # self.df = pd.concat([self.df, df_stat], axis=1)
        # df_stat = pd.read_sql_query(
        #     f'SELECT * FROM activites_stat WHERE IRIS= {IRIS}', con=engine)
        # variables_to_keep = [
        #     "IRIS", "P18_POP1564", "P18_POP1524", "P18_POP2554", "P18_POP5564",
        #     "P18_ACT1564", "P18_ACTOCC1564", "P18_CHOM1564", "C18_ACT1564",
        #     "C18_ACT1564_CS1", "C18_ACT1564_CS3", "C18_ACT1564_CS2",
        #     "C18_ACT1564_CS4", "C18_ACTOCC1564", "C18_ACTOCC1564_CS1",
        #     "C18_ACTOCC1564_CS2", "C18_ACTOCC1564_CS3", "C18_ACTOCC1564_CS4",
        #     "P18_ACTOCC15P_ILT1", "C18_ACTOCC15P", "C18_ACTOCC15P_PAS",
        #     "C18_ACTOCC15P_MAR", "C18_ACTOCC15P_VELO", "C18_ACTOCC15P_2ROUESMOT",
        #     "C18_ACTOCC15P_VOIT", "C18_ACTOCC15P_TCOM"
        # ]
        # df_stat = df_stat[variables_to_keep]
        # self.df = pd.concat([self.df, df_stat], axis=1)
        # return self.df


class FraisCalculation :
    """calcul des frais de notaires et des frais estimés d'agence """

    def __init__ (self, low_result,result,high_result, neuf):
        self.low_result = low_result
        self.result = result
        self.high_result = high_result
        self.neuf = neuf

    def frais_notaires (self):
        if self.neuf == 'Neuf':
            self.frais_notaires_low= round(self.low_result*2.5/100)
            self.frais_notaires_n= round(self.result*2.5/100)
            self.frais_notaires_high = round(self.high_result*2.5/100)
        else:
            self.frais_notaires_low= round(self.low_result*7.5/100)
            self.frais_notaires_n= round(self.result*7.5/100)
            self.frais_notaires_high = round(self.high_result*7.5/100)
        return self.frais_notaires_low, self.frais_notaires_n, self.frais_notaires_high

    def frais_agence (self):
        self.frais_agence_low= round(self.low_result*2.5/100)
        self.frais_agence_n= round(self.result*2.5/100)
        self.frais_agence_high = round(self.high_result*2.5/100)
        return self.frais_agence_low ,self.frais_agence_n , self.frais_agence_high

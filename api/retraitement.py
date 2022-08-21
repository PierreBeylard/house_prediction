from datetime import datetime
import numpy as np

from sklearn.impute import KNNImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer

class prepareReceivedData:

    def __init__(self,df):
        self.df = df

    def dep_and_terrain (self):
        self.df['Dependance'] = str(1) if False else str(0)
        if self.df['main_type_terrain'][0] == 'Champs':
            self.df.at[0,'main_type_terrain'] = 'T'
        elif self.df['main_type_terrain'][0] == 'Verger':
            self.df.at[0,'main_type_terrain'] = 'VE'
        elif self.df['main_type_terrain'][0] == 'Terrain batir':
            self.df.at[0, 'main_type_terrain'] = 'AB'
        else :
            self.df['main_type_terrain'] = 'S'
        return self

    def columns_featuring_act (self) :
        # repartition population
        self.df["Taux_1524"] = self.df["P18_POP1524"]/self.df["P18_POP1564"]
        self.df["Taux_2554"] = self.df["P18_POP2554"]/self.df["P18_POP1564"]
        self.df["Taux_5564"] = self.df["P18_POP5564"]/self.df["P18_POP1564"]
        # statistiques économiques
        self.df["Taux_P_Act"] = self.df["P18_ACT1564"]/self.df["P18_POP1564"]
        self.df["Taux_P_ActOct"] = self.df["P18_ACTOCC1564"]/self.df["P18_ACT1564"]
        self.df["Taux_P_CHO"] = self.df["P18_CHOM1564"]/self.df["P18_ACT1564"]

        self.df["Taux_CS1"] = self.df["C18_ACT1564_CS1"]/self.df["C18_ACT1564"]
        self.df["Taux_CS2"] = self.df["C18_ACT1564_CS2"]/self.df["C18_ACT1564"]
        self.df["Taux_CS3"] = self.df["C18_ACT1564_CS3"]/self.df["C18_ACT1564"]
        self.df["Taux_CS4"] = self.df["C18_ACT1564_CS4"]/self.df["C18_ACT1564"]

        # Statistiques sur transport travail
        self.df["Taux_Travail_Commune"] = self.df["P18_ACTOCC15P_ILT1"]/self.df["P18_ACTOCC1564"]
        self.df["Taux_TT"] = self.df["C18_ACTOCC15P_PAS"]/self.df["C18_ACTOCC15P"]
        self.df["Taux_Mar"] = self.df["C18_ACTOCC15P_MAR"]/self.df["C18_ACTOCC15P"]
        self.df["Taux_Velo"] = self.df["C18_ACTOCC15P_VELO"]/self.df["C18_ACTOCC15P"]
        self.df["Taux_2Roues"] = self.df["C18_ACTOCC15P_2ROUESMOT"]/self.df["C18_ACTOCC15P"]
        self.df["Taux_Voit"] = self.df["C18_ACTOCC15P_VOIT"]/self.df["C18_ACTOCC15P"]
        self.df["Taux_TCOM"] = self.df["C18_ACTOCC15P_TCOM"]/self.df["C18_ACTOCC15P"]


        self.df =self.df.drop(["P18_POP1564", "P18_POP1524","P18_POP2554","P18_POP5564", "P18_ACT1564","P18_ACTOCC1564","P18_CHOM1564",
            "C18_ACT1564", "C18_ACT1564_CS1","C18_ACT1564_CS3","C18_ACT1564_CS2","C18_ACT1564_CS4","C18_ACTOCC1564",
            "C18_ACTOCC1564_CS1" ,"C18_ACTOCC1564_CS2","C18_ACTOCC1564_CS3", "C18_ACTOCC1564_CS4","P18_ACTOCC15P_ILT1","C18_ACTOCC15P",
            "C18_ACTOCC15P_PAS" ,"C18_ACTOCC15P_MAR" ,"C18_ACTOCC15P_VELO" ,"C18_ACTOCC15P_2ROUESMOT" ,"C18_ACTOCC15P_VOIT" ,
            "C18_ACTOCC15P_TCOM"], axis = 1)
        return self

    def columns_featuring_log (self) :
        self.df["Taux_RP"] = self.df["P18_RP"]/self.df["P18_LOG"]
        self.df["Taux_LV"] = self.df["P18_LOGVAC"]/self.df["P18_LOG"]
        self.df["Taux_MAI"] = self.df["P18_MAISON"]/self.df["P18_LOG"]
        # APPARTEMENT PAS UTILE CAR SOIT MAISON SOIT APPARTEMENT
        #nb pieces
        self.df["Taux_RP_1P"] = self.df["P18_RP_1P"]/self.df["P18_RP"]
        self.df["Taux_RP_2P"] = self.df["P18_RP_2P"]/self.df["P18_RP"]
        self.df["Taux_RP_3P"] = self.df["P18_RP_3P"]/self.df["P18_RP"]
        self.df["Taux_RP_4P"] = self.df["P18_RP_4P"]/self.df["P18_RP"]
        self.df["Taux_RP_5P"] = self.df["P18_RP_5PP"]/self.df["P18_RP"]
        #superficie
        self.df["Taux_RP_30"] = self.df["P18_RP_M30M2"]/self.df["P18_RP"]
        self.df["Taux_RP_40"] = self.df["P18_RP_3040M2"]/self.df["P18_RP"]
        self.df["Taux_RP_60"] = self.df["P18_RP_4060M2"]/self.df["P18_RP"]
        self.df["Taux_RP_80"] = self.df["P18_RP_6080M2"]/self.df["P18_RP"]
        self.df["Taux_RP_100"] = self.df["P18_RP_80100M2"]/self.df["P18_RP"]
        self.df["Taux_RP_120"] = self.df["P18_RP_100120M2"]/self.df["P18_RP"]
        self.df["Taux_RP_P120"] = self.df["P18_RP_120M2P"]/self.df["P18_RP"]
        #occupation
        self.df["Taux_RP_GAR"] = self.df["P18_RP_GARL"]/self.df["P18_RP"]
        self.df["Taux_RP_PROPRIO"] = self.df["P18_RP_PROP"]/self.df["P18_RP"]
        self.df["Taux_RP_GRATUIT"] = self.df["P18_RP_GRAT"]/self.df["P18_RP"]
        self.df["Taux_RP_LOC"] = self.df["P18_RP_LOC"]/self.df["P18_RP"]
        self.df["Taux_RP_HML"] = self.df["P18_RP_LOCHLMV"]/self.df["P18_RP"]
        self.df["Taux_RP_AM02"] = self.df["P18_MEN_ANEM0002"]/self.df["P18_RP"]
        self.df["Taux_RP_AM04"] = self.df["P18_MEN_ANEM0204"]/self.df["P18_RP"]
        self.df["Taux_RP_AM09"] = self.df["P18_MEN_ANEM0509"]/self.df["P18_RP"]
        self.df["Taux_RP_AM09P"] = self.df["P18_MEN_ANEM10P"]/self.df["P18_RP"]
        self.df =self.df.drop(['LAB_IRIS','IRIS','P18_LOG', 'P18_RP', 'P18_RSECOCC', 'P18_LOGVAC', 'P18_MAISON', 'P18_APPART','P18_RP_1P',
            'P18_RP_2P', 'P18_RP_3P', 'P18_RP_4P', 'P18_RP_5PP','P18_RP_M30M2', 'P18_RP_3040M2', 'P18_RP_4060M2',
        'P18_RP_6080M2', 'P18_RP_80100M2', 'P18_RP_100120M2', 'P18_RP_120M2P','P18_RP_GARL','P18_RP_PROP',
            'P18_RP_LOC', 'P18_RP_LOCHLMV','P18_RP_GRAT','P18_MEN_ANEM0002', 'P18_MEN_ANEM0204',
        'P18_MEN_ANEM0509', 'P18_MEN_ANEM10P'], axis = 1)
        return self

    def feature_generation (self):
        # convert the 'Date' column to datetime format
        self.df["month"] =  str(datetime.now().month)
        ## attention à ne faire qu'après avoir enrichi avec variables insee
        type_voie_list=['VOIE', 'TRA', 'FG', 'DOM', 'COUR', 'COTE', 'PROM', 'CHS', 'PTR',
        'PARC', 'QUA', 'CR', 'VEN', 'CAMI', 'VGE', 'COR', 'N', 'MAIL',
        'ACH', 'CD', 'ART', 'D', 'CAE', 'RPT', 'CC', 'PLAN', 'ZAC', 'PASS',
        'VCHE', 'PLA', 'VTE', 'ESP', 'PTTE', 'GPL', 'CTR', 'RPE', 'LEVE',
        'ENC', 'TSSE', 'PLE', 'VAL', 'PCH', 'DIG', 'ROC', 'CAR', 'PTE',
        'ZA', 'PRT', 'ESC', 'TOUR', 'CTRE', 'VALL', 'PIST', 'FRM', 'ESPA',
        'DSC', 'DRA', 'PONT', 'REM', 'CORO', 'CHV', 'CHL', 'HAB', 'CALL',
        'RTD', 'VIL', 'PORT', 'PAE', 'VIA', 'ILOT', 'ZI', 'CRX', 'BRG',
        'PRV', 'RUET', 'CASR', 'FOS', 'RIVE', 'ZONE', 'VOIR', 'BSN',
        'RULT', 'HLM', 'VOY', 'MAIS', 'HLG', 'PTA', 'PLT', 'CIVE', 'CLR',
        'NTE', 'PLCI', 'CHT', 'TRT', 'BRE']
        if self.df["type_de_voie"][0] in type_voie_list:
            self.df["type_de_voie"] = "Autres"
        self.df["type_de_voie"]= self.df["type_de_voie"].replace(np.nan,"vide")
        ## correted directly inside train dataset :)
#        self.df["clean_code_commune"] = [c[3:].zfill(3) for c in  self.df["clean_code_commune"]]
        return self.df

## to delete, included in model 
class Pipeline:

    def __init__(self, df):
        self.df = df

    def pipeline(self):
        # création des pipelines de pré-processing pour les variables numériques et catégorielles
        #ajout d'un parametre pour gerer les valeures non connues dans onehotencoder - il les passe à 0(autres options disponibles)
        # Séparation des variables catégorielles et numériques
        categorical_features = [
            "type_de_voie", "clean_code_departement", "clean_code_commune",
            "code_postal", "main_type_terrain", "Dependance", "month"
        ]
        numerical_features = [
            "surface_terrain", "surface_reelle_bati", "nb_pieces_principales",
            'Taux_RP', 'Taux_LV', 'Taux_MAI', 'Taux_RP_1P', 'Taux_RP_2P',
            'Taux_RP_3P', 'Taux_RP_4P', 'Taux_RP_5P', 'Taux_RP_30',
            'Taux_RP_40', 'Taux_RP_60', 'Taux_RP_80', 'Taux_RP_100',
            'Taux_RP_120', 'Taux_RP_P120', 'Taux_RP_GAR', 'Taux_RP_PROPRIO',
            'Taux_RP_GRATUIT', 'Taux_RP_LOC', 'Taux_RP_HML', 'Taux_RP_AM02',
            'Taux_RP_AM04', 'Taux_RP_AM09', 'Taux_RP_AM09P', 'Taux_1524',
            'Taux_2554', 'Taux_5564', 'Taux_P_Act', 'Taux_P_ActOct',
            'Taux_P_CHO', 'Taux_CS1', 'Taux_CS2', 'Taux_CS3', 'Taux_CS4',
            'Taux_Travail_Commune', 'Taux_TT', 'Taux_Mar', 'Taux_Velo',
            'Taux_2Roues', 'Taux_Voit', 'Taux_TCOM'
        ]
        numerical_pipeline = make_pipeline(KNNImputer(n_neighbors=3),
                                           MinMaxScaler())
        categorical_pipeline = make_pipeline(
            OneHotEncoder(handle_unknown="ignore"))
        preprocessor = make_column_transformer(
            (numerical_pipeline, numerical_features),
            (categorical_pipeline, categorical_features))
        model = make_pipeline(preprocessor, LinearRegression())
        fitted_model = model.fit(self.X_train, self.y_train)
        return fitted_model, self.X_train, self.y_train, self.X_test, self.y_test

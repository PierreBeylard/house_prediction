#from house_prediction_package.data import GetData
import pandas as pd
import numpy as np
from datetime import datetime
from more_itertools import chunked
from scipy import stats
from data import ApiEnrichment


from sklearn.model_selection import train_test_split
#sans doute à supprimer au lancement final du modele
#from locale import atof, setlocale, LC_NUMERIC, LC_ALL

#setlocale(LC_ALL, 'fr_FR.UTF-8')

class Preprocessing :

    def __init__(self,df) :
        # self.df = get_data().read_csv()
        self.df = df

    def clean_columns(self,
                      columns=[
                          'Code service CH', 'Reference document',
                          '1 Articles CGI', '2 Articles CGI', '3 Articles CGI',
                          '4 Articles CGI', '5 Articles CGI', 'No Volume',
                          'Identifiant local'
                      ]):
        """ drop useless columns
        Customisation of columns to drop must be entered as a list
        """
        # suppression of 100% empty columns - these columns are officially not completed in this db
        self.df = self.df.drop(columns,axis=1)
        # suppression of columns poorly completed
        columns_to_drop = [column for column in self.df.columns if ((self.df[column].isnull().value_counts()[0]/self.df.shape[0])*100) < 2 ]
        self.df= self.df.drop(columns_to_drop,axis=1)
        # replacement of , by . in numerical variables & deletion of non numrical caracters in num columns :
        columns_num = ['Valeur fonciere', 'Surface Carrez du 1er lot', 'Nombre de lots',
        'Surface reelle bati', 'Nombre pieces principales', 'Surface terrain']
        # transformation des , en . pour réaliser des opérations sur les nombres et suppressions des caracteres non numériques au sein de ces colonnes
        for column in columns_num :
            self.df[column]=self.df[column].apply(lambda s: s.replace(",",".") if isinstance(s,str) else s)
            self.df[column] = pd.to_numeric(self.df[column], errors = 'coerce')
        # suppression of nan value on target variable
        self.df= self.df.dropna(subset=['Valeur fonciere'])
        #self.df['Surface Carrez du 1er lot'] = self.df['Surface Carrez du 1er lot'].apply(
        #    lambda x: atof(x))
        # pre processing avant groupby mais attention sortir valeures foncieres avant de mettre en POO
        ob_columns= self.df.dtypes[self.df.dtypes == 'O'].index
        num_columns = self.df.dtypes[(self.df.dtypes == 'int')
                                     | (self.df.dtypes == 'float')].index
        non_num_col = ['No disposition', 'No voie', 'Code postal', 'Code commune',
        'Prefixe de section', 'No plan','Code type local']
        num_columns = [value for value in num_columns if value not in non_num_col]
        for column in ob_columns :
            self.df[column]=self.df[column].replace(np.nan,'',regex=True)
        #à adapter in v2

        self.df[num_columns] = self.df[num_columns].apply(pd.to_numeric,
                                                              errors='coerce')

        #drop duplicates
        self.df = self.df.drop_duplicates().reset_index(drop= True)
        # by returning self, we can do method chaining like preprocessing(df).clean_columns().create_identifier()
        return self.df

    def create_identifier(self) :
        """ Create a 'unique' identifier allowing us to group several lines corresponding to a unique transaction
        """
        variables_to_clean = [
            "Code departement", "Code commune", "Prefixe de section",
            "Section", "No plan"
            ]
        size_variables= [2,3,3,2,4]
        for i,j in zip(variables_to_clean,size_variables):
            chunked_data = chunked(self.df[i], 10000, strict=False)
            values = {"Prefixe de section": '000'}
            self.df= self.df.fillna(value=values)
            if i == "Prefixe de section" :
                self.df[i] = self.df[i].apply(str).apply(lambda x: x[:3])
            new_variable = [
                str(value).replace(".","").zfill(j) for sublist in chunked_data
                for value in sublist
            ]
            self.df[f"clean_{i.replace(' ','_').lower()}"] = new_variable
            self.df= self.df.drop([i],axis=1)
        self.df["parcelle_cadastrale"] = self.df[[
            "clean_code_departement", "clean_code_commune", "clean_prefixe_de_section",
            "clean_section", "clean_no_plan"]].apply(lambda x: "".join(x), axis=1)
        self.df["parcelle_cad_section"]=self.df["parcelle_cadastrale"].str[:10]
        self.df = self.df.drop([
            "clean_prefixe_de_section", "clean_section", "clean_no_plan"
        ], axis = 1)
        return self.df

    def aggregate_transactions(self):
        self.df = self.df.groupby(["parcelle_cad_section","Date mutation","Valeur fonciere"], as_index= False).apply(lambda x : pd.Series({
            "num_voie" : x["No voie"].max()
            ,"B_T_Q" : x["B/T/Q"].astype(str).max()
            ,"type_de_voie": x["Type de voie"].max()
            ,"voie": x["Voie"].max()
            ,"code_postal": x["Code postal"].max()
            ,"commune": max(x["Commune"])
            ,"clean_code_departement": x["clean_code_departement"].max()
            ,"clean_code_commune": max(x["clean_code_commune"])
            ,"surface_carrez_lot_1" :  x["Surface Carrez du 1er lot"].sum()/((x["Surface reelle bati"].count()/x["Nature culture"].nunique()))
            ,"Nb_lots": x["Nombre de lots"].max()
            ,"surface_terrain" : ((x["Surface terrain"].sum()/x["Surface reelle bati"].count()) if (int(x["Surface terrain"].nunique()) ==1 and int(x["Nature culture"].nunique()) == 1 )else x["Surface terrain"].unique().sum())
            ,"surface_reelle_bati" : (x["Surface reelle bati"].sum()/(x["Surface reelle bati"].count()/x["Type local"].nunique()) if (int(x["Nature culture"].nunique() > 1)) else x["Surface reelle bati"].sum())
            ,"nb_pieces_principales" : (x["Nombre pieces principales"].sum()/(x["Surface reelle bati"].count()/x["Type local"].nunique()) if int(x["Nature culture"].nunique()) > 1 else x["Nombre pieces principales"].sum())
            ,"dependance" : (1 if (len(x["Type local"].unique()) ==1 and x["Type local"].unique()[0] == 'Dépendance') else 0)
            ,"maison" : (1 if (len(x["Type local"].unique()) ==1 and x["Type local"].unique()[0] == 'Maison') else 0)
            ,"appartement": (1 if (len(x["Type local"].unique()) ==1 and x["Type local"].unique()[0] == 'Appartement') else 0)
            ,"multi_locaux":  x["Type local"].unique()
            ,"main_type_terrain" : x["Nature culture"].max()
            ,"parcelle_cadastrale": x["parcelle_cadastrale"].max()}))
        self.df = self.df.replace(np.inf, np.nan)
        # self.df = self.df.replace(np.nan, 0)
        #drop rows with only dependances transactions as we focus on houses
        self.df = self.df[self.df["dependance"]!=1]
        #clean des lignes ou surfaces nulles ou == 0
        self.df = self.df[self.df['surface_terrain']!=0]
        self.df = self.df[self.df['surface_reelle_bati'] != 0]
        return self.df


    def feature_generation (self):
        # convert the 'Date' column to datetime format
        self.df = self.df[self.df['surface_reelle_bati'] != 0]
        self.df["month"] = pd.to_datetime(
            self.df["Date mutation"],format="%d/%m/%Y").dt.month
        self.df= self.df.drop(["Date mutation"], axis = 1)
        ## attention à ne faire qu'après avoir enrichi avec variables insee
        dict_type_voie = dict()
        for value in self.df["type_de_voie"].value_counts()[self.df["type_de_voie"].value_counts()<300 ].index.values :
            dict_type_voie[value] = "Autres"
        self.df=self.df.replace({"type_de_voie" : dict_type_voie})
        self.df["type_de_voie"]= self.df["type_de_voie"].replace(np.nan,'vide')
        self.df["clean_code_commune"]=[c+a[1:] if c[:2]== '97' else (c+a) for c, a in zip(self.df["clean_code_departement"], self.df["clean_code_commune"])]
        self.df["voie"]=self.df["voie"].replace(" ","+")
        self.df["adresse"] = self.df[["num_voie", "type_de_voie", "voie"]].apply(lambda x: "+".join(x.astype(str)), axis=1)
        self.df["adresse"] = self.df[["adresse", "clean_code_commune"]].apply(
            lambda x: "&citycode=".join(x.astype(str)), axis=1)
        self.df["prix_m2"] = self.df["Valeur fonciere"] / self.df[
            "surface_reelle_bati"]
        return self.df

# to do : function calling enrichissement from data
    def enrichissement(self):
        ApiEnrichment(self.df).enrichissement_coordinates(
        ).enrichissement_iris().calcul_superficie().enrichissement_insee()
        return self.df


    def zscore (self) :
        # Calculate the z-score from scratch
        #self.df['Valeur fonciere']= df['Valeur fonciere'].apply(lambda x: atof(x))
        standard_deviation = self.df["Valeur fonciere"].std(ddof=0)
        mean_value = self.df["Valeur fonciere"].mean()
        zscores = [(value - mean_value) / standard_deviation
                for value in self.df["Valeur fonciere"]]
        self.df["zscores"]= zscores
        # absolute value of zscore and if sup x then 1  :
        self.df["outlier"] = [
            1 if (abs(value) > 0.2) else 0 for value in self.df["zscores"]
        ]
        self.df=self.df[self.df["outlier"] == 0].reset_index(drop=True)
        self.df = self.df.drop(["zscores","outlier"], axis = 1)
        return self.df

    def split_x_y (self):
        columns_model = ["type_de_voie",
                         "clean_code_departement",
            "clean_code_commune",
            "code_postal",
            "surface_terrain",
            "surface_reelle_bati", "nb_pieces_principales",
            "main_type_terrain",  "Dependance",'Taux_RP', 'Taux_LV', 'Taux_MAI',
        'Taux_RP_1P', 'Taux_RP_2P', 'Taux_RP_3P', 'Taux_RP_4P', 'Taux_RP_5P',
        'Taux_RP_30', 'Taux_RP_40', 'Taux_RP_60', 'Taux_RP_80', 'Taux_RP_100',
        'Taux_RP_120', 'Taux_RP_P120', 'Taux_RP_GAR', 'Taux_RP_PROPRIO',
        'Taux_RP_GRATUIT', 'Taux_RP_LOC', 'Taux_RP_HML', 'Taux_RP_AM02',
        'Taux_RP_AM04', 'Taux_RP_AM09', 'Taux_RP_AM09P','Taux_1524',
        'Taux_2554', 'Taux_5564', 'Taux_P_Act', 'Taux_P_ActOct', 'Taux_P_CHO',
        'Taux_CS1', 'Taux_CS2', 'Taux_CS3', 'Taux_CS4', 'Taux_Travail_Commune',
        'Taux_TT', 'Taux_Mar', 'Taux_Velo', 'Taux_2Roues', 'Taux_Voit',
        'Taux_TCOM',
        'month']
        # Séparation des variables catégorielles et numériques
        categorical_features = [
            "type_de_voie",
             "clean_code_departement",
            "clean_code_commune","code_postal",
             "main_type_terrain", "Dependance", "month"
        ]
        numerical_features = [
            "surface_terrain", "surface_reelle_bati", "nb_pieces_principales",'Taux_RP', 'Taux_LV', 'Taux_MAI',
        'Taux_RP_1P', 'Taux_RP_2P', 'Taux_RP_3P', 'Taux_RP_4P', 'Taux_RP_5P',
        'Taux_RP_30', 'Taux_RP_40', 'Taux_RP_60', 'Taux_RP_80', 'Taux_RP_100',
        'Taux_RP_120', 'Taux_RP_P120', 'Taux_RP_GAR', 'Taux_RP_PROPRIO',
        'Taux_RP_GRATUIT', 'Taux_RP_LOC', 'Taux_RP_HML', 'Taux_RP_AM02',
        'Taux_RP_AM04', 'Taux_RP_AM09', 'Taux_RP_AM09P','Taux_1524',
        'Taux_2554', 'Taux_5564', 'Taux_P_Act', 'Taux_P_ActOct', 'Taux_P_CHO',
        'Taux_CS1', 'Taux_CS2', 'Taux_CS3', 'Taux_CS4', 'Taux_Travail_Commune',
        'Taux_TT', 'Taux_Mar', 'Taux_Velo', 'Taux_2Roues', 'Taux_Voit',
        'Taux_TCOM'
        ]
        for column in categorical_features:
            self.df[column] = self.df[column].replace(np.nan, "").apply(str)
        X = self.df[columns_model]
        y =self.df["Valeur fonciere"]
        # selection des variables
        X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                            test_size=0.33,
                                                            random_state=42)
        return self.df,categorical_features, numerical_features, X_train, X_test, y_train, y_test

import pandas as pd
import requests
from sqlalchemy import create_engine

class GetData:
    """ Read data from csv and load it in a dataframe
    accepted arguments : path to file , separator, chunksize and filter
    option to load csv by filtering on house type
    """

    def __init__(self,path ="../data/valeursfoncieres-2021.txt",sep = "|", chunksize = 100000):
        self.path = path
        self.sep = sep
        self.chunksize = chunksize


    def read_csv(self, filtering_column='Code type local', filter=[1]):
        """ pass option on which column to filter and filter value
        if several filter value, pass the as a list"""
        iter_csv = pd.read_csv(self.path,
                               sep=self.sep,
                               iterator=True,
                               chunksize=self.chunksize,
                               low_memory=False)
        self.df = pd.concat([
            chunk[chunk[filtering_column].isin(filter)] for chunk in iter_csv
        ])
        return self.df

    def enrichissement_coordinates(self,df):
        pass

    def enrichissement_insee(self,df):
        pass


class loading_data_in_db:
    """ class helping to load data into a database
    please enter db name as second argument
    please enter table name as third argument"""

    def __init__(self, df, db_name, table_name):
        self.df = df
        self.db_name = db_name
        self.table_name = table_name

    def load_df_db(self):
        engine = create_engine(f'sqlite:///../data/{self.db_name}.sqlite',
                               echo=True)  # pass your db url
        self.df.to_sql(name=self.table_name,
                       con=engine,
                       if_exists='replace',
                       index=False)


class apiEnrichment:
    """Objective : obtain latitude, longitude from 2 apis :
    https://adresse.data.gouv.fr/api-doc/adresse --- to normalize & obtain coordinates from an address
    https://pyris.datajazz.io/ --for IRIS
    """

    def __init__(self,df
                 addresse):
        self.df = df
  #      self.addresse = addresse

    def enrichissement_coordinates(self):
        result = requests.get(
                f'https://api-adresse.data.gouv.fr/search/?q={self.df["addresse"]}').json(
                )['features'][0]['geometry']['coordinates']
        long =[]
        lat =[]
        try :
            long.append(result[0])
            lat.append(result[1])
        except :
            long.append('not found')
            lat.append('not found')
        self.df['coordinates'] = lat+"&lon="+long
        return self

    def enrichissement_iris_insee(self):
        IRIS=[]
        for dep, city, coord in zip(self.df["clean_code_departement"], self.df["clean_code_commune"], self.df["coordinates"]):
            if dep == '971':
                url =f"https://regionguadeloupe.opendatasoft.com/api/records/1.0/search/?dataset=iris-millesime-france&q={city}&sort=year&facet=com_arm_name"
                try:
                    IRIS.append(requests.get(
                        f'{url}').json()['records'][0]['fields']['iris_code'])
                except:
                    IRIS.append('not found')
            elif dep == '972' or dep == '973' :
                url = f"https://public.opendatasoft.com/api/records/1.0/search/?dataset=georef-france-iris&q={city}&sort=year&facet=com_arm_name"
                try:
                    IRIS.append(requests.get(
                        f'{url}').json()['records'][0]['fields']['iris_code'])
                except:
                    IRIS.append('not found')
            elif dep == '974':
                url = f"https://data.opendatasoft.com/api/records/1.0/search/?dataset=iris-millesime-france%40lareunion&q={city}&sort=year&facet=com_arm_name"
                try:
                    IRIS.append(requests.get(
                        f'{url}').json()['records'][0]['fields']['iris_code'])
                except:
                    IRIS.append('not found')
            else :
                url = "https://pyris.datajazz.io/api/coords?geojson=false&lat="
                try:
                    IRIS.append(requests.get(
                    f'{url}{coord}').json()['complete_code'])
                except:
                    IRIS.append('not found')

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

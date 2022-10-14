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


class LoadingDataInDb:
    """ class helping to load data into a database
    please enter db name as second argument
    please enter table name as third argument
    """

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


class ApiEnrichment:
    """Objective : obtain latitude, longitude from 2 apis :
    https://adresse.data.gouv.fr/api-doc/adresse --- to normalize & obtain coordinates from an address
    https://pyris.datajazz.io/ --for IRIS
    """

    def __init__(self,df):
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

    def enrichissement_iris(self):
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
        return self

    def calcul_superficie(self):
        # Connection à sqlite pour récupérer les IRIS Métropole et DOM
        engine = create_engine('sqlite:///../data/house_pred_database.sqlite',
                               echo=True)
        df_IRIS=pd.read_sql_query(
            f'SELECT IRIS,substr(COM,1,3) as clean_code_departement FROM logements_stats', con=engine)
        IRIS = tuple(df_IRIS['IRIS'].unique())
        # Connection à la base PostgreSQL pyris
        engine = create_engine('postgresql://postgres:secret@localhost/pyris')
        df_IRIS_M = pd.read_sql_query(
            f"SELECT *,ST_Area(geom::GEOGRAPHY) as superficie_m2 FROM geoiris where code_iris in {IRIS}",
            con=engine)
        df_IRIS = df_IRIS.merge(df_IRIS_M[['code_iris', 'superficie_m2']],
                                left_on='IRIS',
                                right_on='code_iris',
                                suffixes=('_left', '_right'),
                                how='left')
        # IRIS = tuple(df_IRIS_M[df_IRIS_M.superficie_m2.isnull()].IRIS.unique())
        for index, value in df_IRIS[df_IRIS.superficie_m2.isnull()].iterrows():
            if value['clean_code_departement'] =='974' :
                df_IRIS.at[index,'superficie_m2'] = pd.read_sql_query(f'SELECT ST_Area(st_setSRID(geometry,4326)::GEOGRAPHY) as superficie_m2 FROM reu_2022 where "CODE_IRIS" = {value["IRIS"]}::TEXT', con = engine)['superficie_m2'][0]
            elif value['clean_code_departement'] =='971':
                df_IRIS.at[index,'superficie_m2'] = pd.read_sql_query(f'SELECT ST_Area(st_setSRID(geometry,4326)::GEOGRAPHY) as superficie_m2 FROM glp_2022 where "CODE_IRIS" = {value["IRIS"]}::TEXT', con = engine)['superficie_m2'][0]
            elif value['clean_code_departement'] =='972':
                df_IRIS.at[index,'superficie_m2'] = pd.read_sql_query(f'SELECT ST_Area(st_setSRID(geometry,4326)::GEOGRAPHY) as superficie_m2 FROM mtq_2022 where "CODE_IRIS" = {value["IRIS"]}::TEXT', con = engine)['superficie_m2'][0]
            elif value['clean_code_departement'] =='973':
                df_IRIS.at[index,'superficie_m2'] = pd.read_sql_query(f'SELECT ST_Area(st_setSRID(geometry,4326)::GEOGRAPHY) as superficie_m2 FROM guf_2022 where "CODE_IRIS" = {value["IRIS"]}::TEXT', con = engine)['superficie_m2'][0]
            else :
                df_IRIS.at[index,'superficie_m2'] = 'NOT FOUND'
        LoadingDataInDb(df_IRIS, 'house_pred_database',
                           'IRIS_superficie').load_df_db()
        return self



    def enrichissement_insee(self):
        IRIS = tuple(self.df['IRIS'])
        engine = create_engine('sqlite:///../data/house_pred_database.sqlite',
                               echo=True)

        variables_to_keep = [
        'IRIS', 'LAB_IRIS','P18_LOG', 'P18_RP', 'P18_RSECOCC', 'P18_LOGVAC',
        'P18_MAISON', 'P18_APPART','P18_RP_1P', 'P18_RP_2P', 'P18_RP_3P',
        'P18_RP_4P', 'P18_RP_5PP','P18_NBPI_RP','P18_RP_M30M2', 'P18_RP_3040M2', 'P18_RP_4060M2',
       'P18_RP_6080M2', 'P18_RP_80100M2', 'P18_RP_100120M2', 'P18_RP_120M2P','P18_RP_GARL','P18_RP_PROP',
         'P18_RP_LOC', 'P18_RP_LOCHLMV','P18_RP_GRAT','P18_MEN_ANEM0002', 'P18_MEN_ANEM0204',
       'P18_MEN_ANEM0509', 'P18_MEN_ANEM10P','P18_RP_ACHTOT', 'P18_RP_ACH19', 'P18_RP_ACH45', 'P18_RP_ACH70',
       'P18_RP_ACH90', 'P18_RP_ACH05', 'P18_RP_ACH15'
        ]
        df_stat = pd.read_sql_query(
            f'SELECT * FROM logements_stats', con=engine)
        df_stat = df_stat[variables_to_keep]
        variables_to_keep = [
            "IRIS","P18_POP1564", "P18_POP1524", "P18_POP2554", "P18_POP5564",
            "P18_ACT1564", "P18_ACTOCC1564", "P18_CHOM1564", "C18_ACT1564",
            "C18_ACT1564_CS1", "C18_ACT1564_CS3", "C18_ACT1564_CS2",
            "C18_ACT1564_CS4", "C18_ACTOCC1564", "C18_ACTOCC1564_CS1",
            "C18_ACTOCC1564_CS2", "C18_ACTOCC1564_CS3", "C18_ACTOCC1564_CS4",
            "P18_ACTOCC15P_ILT1", "C18_ACTOCC15P", "C18_ACTOCC15P_PAS",
            "C18_ACTOCC15P_MAR", "C18_ACTOCC15P_VELO", "C18_ACTOCC15P_2ROUESMOT",
            "C18_ACTOCC15P_VOIT", "C18_ACTOCC15P_TCOM"
        ]
        df_stat2 = pd.read_sql_query(
            f'SELECT * FROM activites_stat', con=engine)
        df_stat2 = df_stat2[variables_to_keep]
        df_stat = df_stat.merge(df_stat2,
                                left_on='IRIS',
                                right_on='IRIS',
                                suffixes=('_left', '_right'),
                                how='left')

        df_stat2 = pd.read_sql_query(
            f'SELECT * FROM IRIS_superficie',
            con=engine)
        variables_to_keep = [
            "IRIS", "superficie_m2"
        ]
        df_stat2 = df_stat2[variables_to_keep]
        df_stat = df_stat.merge(df_stat2,
                                left_on='IRIS',
                                right_on='IRIS',
                                suffixes=('_left', '_right'),
                                how='left')

        df_stat2 = pd.read_sql_query(
            f'SELECT * FROM population_stat', con=engine)

        df_stat = df_stat.merge(df_stat2,
                                left_on='IRIS',
                                right_on='IRIS',
                                suffixes=('_left', '_right'),
                                how='left')
        df_stat['superficie_m2']=df_stat['superficie_m2'].replace('', np.nan).apply(pd.to_numeric, errors='coerce')
        df_stat['densite_pop'] = df_stat['P18_POP'] / (
            df_stat['superficie_m2'] / 1000000)
        df_stat['nb_pieces_moyen'] = df_stat["P18_NBPI_RP"]/df_stat['P18_RP']
        LoadingDataInDb(df_stat, 'house_pred_database',
                           'INSEE_MODEL_STAT').load_df_db()
        self.df = self.df.merge(df_stat,
                                left_on='IRIS',
                                right_on='IRIS',
                                suffixes=('_left', '_right'),
                                how='left')
        return self.df

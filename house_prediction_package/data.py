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


class api_enrichment :
    """Objective : obtain latitude, longitude from 2 apis :
    https://adresse.data.gouv.fr/api-doc/adresse --- to normalize & obtain coordinates from an address
    https://pyris.datajazz.io/ --for IRIS
    """

    def __init__(self,
                 addresse):
        self.addresse = addresse

    def enrichissement_coordinates(self):
        try :
            long = requests.get(
                f'https://api-adresse.data.gouv.fr/search/?q={self.addresse}').json(
                )['features'][0]['geometry']['coordinates'][0]
            lat = requests.get(
                f'https://api-adresse.data.gouv.fr/search/?q={addresse_for_enrichment}').json(
                )['features'][0]['geometry']['coordinates'][1]
        except :
            long = 'not found'
            lat = 'not found'
        return self

    def enrichissement_iris(self):
        coordinates = (str(self.lat), str(self.long))
        coordinates = "&lon=".join(coordinates)
        pyris_api_url = "https://pyris.datajazz.io/api/coords?geojson=false&lat="
        try:
            self.IRIS = requests.get(
                f'{pyris_api_url}{coordinates}').json()['complete_code']
        except:
            self.IRIS = 'not found'
        return self.IRIS

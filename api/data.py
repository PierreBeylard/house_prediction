import pandas as pd
import requests
from sqlalchemy import create_engine

class loadingDataInDb:
    """ class helping to load data into a database
    each time a demand is passed, data is uploaded into database
    please enter db name as second argument
    please enter table name as third argument"""

    def __init__(self, df, db_name, table_name, result):
        self.df = df
        self.db_name = db_name
        self.table_name = table_name
        self.result = result

    def load_df_db(self):
        self.df['result']= self.result
        engine = create_engine(f'sqlite:///../data/{self.db_name}.sqlite',
                               echo=True)  # pass your db url
        self.df.to_sql(name=self.table_name,
                       con=engine,
                       if_exists='append',
                       index=False)
        engine.dispose()

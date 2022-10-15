import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ.get('DB_STRING')
DATABASE_NAME = os.environ.get('DB_NAME')

class LoadingDataInDb:
    """ class helping to load data into a database
    each time a demand is passed, data is uploaded into database
    please enter db name as second argument
    please enter table name as third argument
    """

    def __init__(self, df, db_name, table_name, iris, result):
        self.df = df
        self.db_name = db_name
        self.table_name = table_name
        self.iris = iris
        self.result = result

    def load_df_db(self):
        self.df['result']= self.result
        self.df['iris']= self.iris
        self.df['date_demande'] = pd.to_datetime("today")
        engine = create_engine(f'sqlite:///../data/{DATABASE_NAME}.sqlite',
                               echo=True)  # pass your db url
        self.df.to_sql(name=self.table_name,
                       con=engine,
                       if_exists='append',
                       index=False)
        engine.dispose()

    def load_df_db_psql (self) :
        self.df['result'] = self.result
        self.df['iris'] = self.iris
        self.df['date_demande'] = pd.to_datetime("today")
        engine = create_engine(f'{DATABASE_URL}{DATABASE_NAME}',
                               echo=True)  # pass your db url
        self.df.to_sql(name=self.table_name,
                       con=engine,
                       if_exists='append',
                       index=False)
        engine.dispose()

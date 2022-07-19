import pandas as pd

class get_data:
    """ Read data from csv and load it in a dataframe
    accepted arguments : path to file , separator, chunksize and filter
    option to load csv by filtering on house type
    """

    def __init__(self,path ="../data/valeursfoncieres-2021.txt",sep = "|", chunksize = 100000):
        self.path = path
        self.sep = sep
        self.chunksize = chunksize


    def read_csv(self, filtering_column='Code type local', filter=1):
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

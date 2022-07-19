from house_prediction_package.data import get_data
from more_itertools import chunked

class preprocessing :

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
        columns_to_drop = [column for column in self.df.columns if ((self.df[column].isnull().value_counts().sort_index()[0]/self.df.shape[0])*100) < 2 ]
        self.df= self.df.drop(columns_to_drop,axis=1)
        # suppression of nan value on target variable
        self.df= self.df.dropna(subset='Valeur fonciere')
        # by returning self, we can do method chaining like preprocessing(df).clean_columns().create_identifier()
        return self

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
                str(value).zfill(j) for sublist in list(chunked_data)
                for value in sublist
            ]
            self.df[f"clean_{i.replace(' ','_').lower()}"] = new_variable
            self.df= self.df.drop([i],axis=1)
        self.df["parcelle_cadastrale"] = self.df[[
            "clean_code_departement", "clean_code_commune", "clean_prefixe_de_section",
            "clean_section", "clean_no_plan"]].apply(lambda x: "".join(x), axis=1)
        self.df["parcelle_cad_section"]=self.df["parcelle_cadastrale"].str[:10]
        self.df = self.df.drop([
            "clean_code_departement", "clean_code_commune",
            "clean_prefixe_de_section", "clean_section", "clean_no_plan"
        ], axis = 1)
        return self.df

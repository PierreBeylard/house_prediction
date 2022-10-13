import numpy as np
import pandas as pd

from sklearn.impute import KNNImputer
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, MinMaxScaler, RobustScaler
from sklearn.model_selection import cross_val_score, learning_curve
from sklearn.linear_model import LinearRegression
from sklearn import pipeline
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer

import warnings
warnings.filterwarnings('ignore')

from house_prediction_package.preprocessing import Preprocessing
from house_prediction_package.data import GetData


class Pipeline :

    def __init__(self, df):
        self.df = df
        # self.categorical_features = categorical_features
        # self.numerical_features = numerical_features
        # self.X_train = X_train
        # self.y_train = y_train
        # option 2
        #appeler les méthodes
        self.df, self.categorical_features, self.numerical_features, self.X_train, self.X_test, self.y_train, self.y_test = Preprocessing(
            df).feature_generation().zscore().split_x_y()

    def pipeline(self):
        # création des pipelines de pré-processing pour les variables numériques et catégorielles
        #ajout d'un parametre pour gerer les valeures non connues dans onehotencoder - il les passe à 0(autres options disponibles)
        numerical_pipeline = make_pipeline(KNNImputer(n_neighbors=3), MinMaxScaler())
        categorical_pipeline = make_pipeline(OneHotEncoder(handle_unknown="ignore"))
        preprocessor = make_column_transformer(
            (numerical_pipeline, self.numerical_features),
            (categorical_pipeline, self.categorical_features))
        model = make_pipeline(preprocessor, LinearRegression())
        fitted_model = model.fit(self.X_train, self.y_train)
        return fitted_model, self.X_train, self.y_train,self.X_test, self.y_test

from sklearn.metrics import classification_report, plot_confusion_matrix
from sklearn.model_selection import cross_val_score

from house_prediction_package.preprocessing import Preprocessing
from house_prediction_package.data import GetData
from house_prediction_package.pipeline import Pipeline


class ML:

    def __init__(self):
        self.df = GetData().read_csv()
        self.X_train, self.X_test, self.y_train, self.y_test = Preprocessing(
        ).select_x_y()
        self.reg = PipelineClass().creation_pipeline()

    def model_fitting(self):
        fitted_model = self.reg.fit(self.X_train, self.y_train)
        return fitted_model

    def model_predict_test(self, X=None):
        fitted_model = self.model_fitting()
        if X is None:
            y_pred = fitted_model.predict(self.X_test)
        else:
            y_pred = fitted_model.predict(X)
        return y_pred, fitted_model

    def model_score(self):
        y_pred, fitted_model = self.model_predict_test()
        accuracy_score = fitted_model.score(self.X_test, self.y_test)
        class_report = classification_report(self.y_test, y_pred)
        conf_matrix = plot_confusion_matrix(fitted_model, self.X_test,
                                            self.y_test).figure_
        scores_cross = cross_val_score(fitted_model,
                                       self.X_test,
                                       self.y_test,
                                       cv=5)
        return accuracy_score, class_report, conf_matrix, scores_cross

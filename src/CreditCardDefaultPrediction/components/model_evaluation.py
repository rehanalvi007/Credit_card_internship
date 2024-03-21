import os
import sys
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from src.CreditCardDefaultPrediction.logger import logging
from src.CreditCardDefaultPrediction.exception import CustomException
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
from src.CreditCardDefaultPrediction.utils.utils import load_object
class ModelEvaluation:
    def __init__(self):
        logging.info("evaluation started")

    def eval_metrics(self,actual,pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))# here is RMSE
        mae = mean_absolute_error(actual, pred)# here is MAE
        r2 = r2_score(actual, pred)# here is r3 value
        logging.info("evaluation metrics captured")
        return rmse, mae, r2


    def initiate_model_evaluation(self, train_array, test_array):
        try:
            X_test, y_test = (test_array[:, :-1], test_array[:, -1])

            model_path = os.path.join("artifacts", "model.pkl")
            model = load_object(model_path)

            mlflow.set_registry_uri("https://dagshub.com/rehanalvi007/Credit_card_internship.mlflow")
            
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
            print(tracking_url_type_store)

            with mlflow.start_run():

                prediction=model.predict(X_test)

                (rmse,mae,r2)=self.eval_metrics(y_test,prediction)

                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)

                #This condition is for dagshub
                if tracking_url_type_store != "file":
                    mlflow.sklearn.log_model(model, "model", registered_model_name="ml_model")
                #This condition is for local    
                else:
                    mlflow.sklearn.log_model(model, "model")
        except Exception as e:
            raise e
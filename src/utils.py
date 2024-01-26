# Here we will write the code which is common to the entire application. e.g Saving my model in the cloud then I will write the code here, read the dataset from the database then I will create my mogodb client here.


import os
import sys
import numpy as np
import pandas as pd
import dill # Library which is also used to create pickle file
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj: # wb means write byte mode. So here we are opening the file path in write byte mode
            pickle.dump(obj, file_obj) # Dump helps to save in the specific file path
    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report={}
         # go through each and every model 
        for i in range(len(list(models))):
            model=list(models.values())[i] # getting each and every model
            para=param[list(models.keys())[i]]

            gs=GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train) # Train the model

            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)

            train_model_score=r2_score(y_train, y_train_pred) # r2_score is used to find the predictions
            test_model_score=r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]]=test_model_score
        return report
    except Exception as e:
        raise CustomException(e, sys)
    

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    
    except Exception as e:
        raise CustomException(e, sys)
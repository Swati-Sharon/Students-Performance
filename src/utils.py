#all common method that entire project can use 
import os
import sys
import numpy as np 
import pandas as pd
#to create a pickle file
import dill
import pickle


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)
        #file path is declared in model_trainer.py
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
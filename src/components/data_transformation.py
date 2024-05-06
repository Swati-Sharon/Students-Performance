import os
import sys
import pandas as pd
import numpy as np
#for pipelines
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
#for data cleaning
from sklearn.impute import SimpleImputer
from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            num_col=['writing score','reading score']
            cat_col=['gender','race/ethnicity','parental level of education','lunch','test preparation course',]


            #for handling missing values
            num_pipeline=Pipeline(steps=[("imputer",SimpleImputer(strategy="median")),
                                         ("scaler",StandardScaler())
                                         ])
            
            cat_pipeline=Pipeline(steps=[("imputer",SimpleImputer(strategy="most_frequent")),
                                         ("one_hot_encoder",OneHotEncoder()),
                                         ("scaler",StandardScaler(with_mean=False))
                                         ])
            logging.info(f"Numerical columns: {num_col}")
            logging.info(f"Categorical columns: {cat_col}")
            

            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,num_col),
                    ("cat_pipeline",cat_pipeline,cat_col),
                ]
            )
            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("read train and test data completed")
            logging.info("obtaianing preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math score"
            num_col=["writing score","reading score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(f"Applying preprocessinng object on traing dataframe and testing dataframe")

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.fit_transform(input_feature_test_df)

            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]
            logging.info(f"Saved preprocessing object")

            save_object(file_path=self.data_transformation_config.preprocessor_obj_file_path,
                        obj=preprocessing_obj)

            return(train_arr,
                   test_arr,self.data_transformation_config.preprocessor_obj_file_path)

        except Exception as e:
            raise CustomException(e,sys)
           
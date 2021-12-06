"""
Diamond-mate

Alf-arv, 2021
"""
import keras
from utilities import one_hot_encode
from keras.models import load_model
import os
import json
import numpy as np
import pandas as pd


# Added to suppress certain hardware-bound errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def infer_single_price(model: keras.models=None, data: pd.DataFrame=None) -> float:
    """
    Function to perform a single diamond price inference using a given model
    :param data: Diamond properties as a dictionary

    @return: The predicted price
    """

    # Make prediction
    prediction = model.predict(data)

    # Check prediction's legitimity
    #TODO: perform this check if possible

    # Return prediction or throw exception
    if prediction is None:
        raise Exception('Error occurred during prediction')
    return prediction[0]


def do_inference(model_path: str=None, data: dict=None) -> float:
    """
    Function to import model from the provided path, and pass the inference job ahead to the relevant function
    :param arg_model:
    :param data:

    @return: result of prediction
    """

    # Fault check
    if data:
        if None in data or len(data.keys()) != 5:
            raise Exception('Data dictionary has wrong shape or contains None.')
    if not model_path:
        raise Exception('No model was provided, or it was provided incorrectly.')

    # Import the model from provided path
    try:
        imported_model = load_model(os.path.join(model_path, 'regression_estimator.h5'), custom_objects=None, compile=True)
    except:
        raise Exception('Model could not be loaded from the provided file path')

    # Single price inference
    else:
        # Transform data dict to compatible dataframe
        for k, v in data.items():
            data[k] = list([v])
        data = pd.DataFrame(data)

        # OHE
        data_df = one_hot_encode(data)

        # add the missing columns
        try:
            original_cols = json.load(open(os.path.join(model_path, 'model_properties.json'), 'r'))
        except:
            raise Exception('model_properties.json could not be loaded')

        extended_data_df = pd.DataFrame([[-1]*30], columns=original_cols['features'])

        # match up columns to the structure that the model expects, fill with zeros
        for i in original_cols['features']:
            if i in data_df.columns:
                extended_data_df[i] = data_df[i][0]
            else:
                extended_data_df[i] = 0

        # Infer the price
        result = infer_single_price(imported_model, extended_data_df)

    return result


def do_batch_inference(model_path:str=None, data: dict=None) -> dict:
    """
    Function to import model from the provided path, and pass the inference job
    to infer_single_price row by row

    :param arg_model:
    :param data:

    @return: result of prediction
    """

    # Import the model from provided path
    try:
        imported_model = load_model(os.path.join(model_path, 'regression_estimator.h5'), custom_objects=None, compile=True)
    except:
        raise Exception('Model could not be loaded from the provided file path')

    #TODO: go through data dict row by row and infer single prices
    #TODO: return dict with list of all diamond's information together with their inferred prices
    return -1

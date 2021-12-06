"""
Diamond-Mate-Backend

Alf-arv, 2021
"""
import keras
from utilities import one_hot_encode, create_inference_input
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

    # Return prediction or throw exception
    if prediction is None:
        raise Exception('Error occurred during prediction')
    return prediction[0]


def do_inference(model_path: str=None, data: dict=None) -> float:
    """
    Function to import model from the provided path, and pass the inference job ahead to the relevant function
    :param model_path: path to model files
    :param data: dictionary with diamond properties

    @return: result of prediction
    """

    # Fault check
    if not model_path:
        raise Exception('No model was provided, or it was provided incorrectly.')

    # Import the model from provided path
    try:
        imported_model = load_model(os.path.join(model_path, 'regression_estimator.h5'), custom_objects=None, compile=True)
    except:
        raise Exception('Model could not be loaded from the provided file path')

    # reshape data
    data = create_inference_input(data)

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

    return float(result)


def do_batch_inference(model_path:str=None, data: dict=None) -> dict:
    """
    Function to import model from the provided path, and pass the inference job
    to infer_single_price row by row

    :param arg_model:
    :param data:

    @return: result dictionary
    """
    # Unstringify the batch
    data['batch'] = json.loads(data['batch'])

    # Fail if structure is wrong
    try:
        data['batch'][0]['Shape']
    except:
        return False

    # For each diamond in the batch, do inference and build response dictionary
    predictions = {}
    for n in range(len(data['batch'])):
        predictions["diamond_"+str(n+1)] = {}
        result = do_inference(model_path, data['batch'][n])
        predictions["diamond_"+str(n+1)]['details'] = data['batch'][n]
        predictions["diamond_"+str(n+1)]['price_prediction'] = result

    return predictions

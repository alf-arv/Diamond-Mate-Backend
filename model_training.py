"""
Diamond-mate-backend

Alf-arv, 2021
"""
import os
import pandas as pd
import json
from utilities import one_hot_encode
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from keras.models import save_model
from keras.optimizers import Adam

def train_regression_estimator(database_path: str=None, model_save_path: str=None):
    """
    Function for training a model to predict/estimate price of input diamond based on properties
    Exports trained model to model/regression_estimator.

    @return: True if successful training and export, False otherwise
    """

    # Import dataset
    pure_dataset = pd.read_csv(database_path, delimiter=';', index_col=False)

    # Binarize categorical columns
    data = one_hot_encode(pure_dataset)

    y = data['Price']
    del data['Price']
    X = data

    x_train, x_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=0.15)

    # Construct neural network
    model = Sequential()
    model.add(Dense(30, input_dim=X.shape[1], activation='relu'))#TODO: Optimize further
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1))

    # Compile and fit model
    model.compile(optimizer=Adam(learning_rate=0.001), loss = 'mse', metrics=['accuracy'])
    model.fit(x_train.values, y_train.squeeze().values, epochs=100, batch_size=5) #TODO: optimize hyperparameters

    # Evaluate model
    accuracy = model.evaluate(x_train, y_train)#TODO: Should the accuracy be saved?

    # Save model features for JSON export
    features = list(X.columns)

    # Save model
    try:
        save_model(model, filepath=os.path.join(model_save_path,'regression_estimator.h5'))
        # export features as json
        with open(os.path.join(model_save_path,'model_properties.json'), 'w') as json_file:
            json.dump({"features": list(features)}, json_file)
    except:
        return False
    return True

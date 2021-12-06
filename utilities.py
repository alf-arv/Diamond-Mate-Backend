"""
Diamond-Mate-Backend

Alf-arv, 2021
"""
import pandas as pd
import random as rd

def one_hot_encode(data: pd.DataFrame=None) -> pd.DataFrame:
    """
    One hot encode input DataFrame

    :param data: input DataFrame
    @return DataFrame with categorical data one-hot-encoded
    """

    binarized_shape = pd.get_dummies(data['Shape'], prefix='shape')
    binarized_clarity = pd.get_dummies(data['Clarity'], prefix='clarity')
    binarized_color = pd.get_dummies(data['Color'], prefix='color')
    binarized_cut = pd.get_dummies(data['Cut'], prefix='cut')

    new_data = data.join(binarized_shape).join(binarized_clarity).join(binarized_color).join(binarized_cut)
    del new_data['Shape']
    del new_data['Clarity']
    del new_data['Color']
    del new_data['Cut']

    return new_data


def create_inference_input(data: dict=None) -> pd.DataFrame:
    """
    Transform data dict to compatible dataframe

    :param data: request dictionary
    @return DataFrame ready for inference
    """

    # fault check
    if data['Shape'] == None or data['Carat'] == None or data['Color'] == None or data['Cut'] == None or data['Clarity'] == None:
        raise Exception('Data dictionary has wrong shape or contains None.')

    for k, v in data.items():
        data[k] = list([v])

    return pd.DataFrame(data)



def determine_pricing_classes(dataset: pd.DataFrame=None) -> pd.Series:
    """
    Function for determining the pricing classes based on percentiles internally in the dataset

    :param dataset: DataFrame of the diamond database to classify
    @return: Pandas series with the pricing categories
    """

    # TODO: In the future

    return np.series(None) # TODO: change


def generate_test_database(size: int=100):
    # Enums
    shapes = ['Round', 'Princess', 'Cushion', 'Emerald', 'Oval', 'Radiant', 'Asscher', 'Marquise', 'Heart', 'Pear']
    colors = ['M', 'L', 'K', 'J', 'I', 'H', 'G', 'F', 'E', 'D']
    clarities = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF', 'FL']
    cuts = ['Good', 'Very Good', 'Ideal']
    creation = ['Lab grown', 'Natural']

    # continous vars
    """
    Price in [100, 4 000 000] €
    Carat in [0.25, 5]
    """

    generated_entries = pd.DataFrame(columns=['Shape', 'Color', 'Clarity', 'Cut', 'Carat', 'Creation', 'Price'])

    for i in range(size):
        generated_entries =generated_entries.append({'Shape': rd.sample(shapes, 1)[0],
                                        'Color': rd.sample(colors, 1)[0],
                                        'Clarity': rd.sample(clarities, 1)[0],
                                        'Cut': rd.sample(cuts, 1)[0],
                                        'Carat': 0.25+rd.random()*4.95,
                                        'Creation': rd.sample(creation, 1)[0],
                                        'Price': 100+round(rd.random(), ndigits=4)*1000000}, ignore_index=True)

    generated_entries.to_csv(os.path.join('data', 'database.csv'))

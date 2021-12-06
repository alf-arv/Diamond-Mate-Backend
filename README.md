# Diamond Mate REST backend

Flask REST-Api for getting ML-calculated diamond price predictions based on the provided parameters.

Scrape diamond sales from the big online sellers of loose diamonds, train a price prediction model, and evaluate pricing on unseen constellations of diamond properties. Don't get ripped off by your local jeweller!

*I recommend to exclusively train with and consider GIA certified diamonds for more consistent pricing.*

## Endpoints

#### (GET) /single_inference
Parameters:

| Name    | Type   | Description                |
|---------|--------|----------------------------|
| Shape   | String | Diamond shape, Ex: "Round" |
| Color   | String | Color grade, Ex: "F"       |
| Clarity | String | Clarity, Ex: "VVS1"        |
| Cut     | String | Cut grade, Ex: "Ideal"     |
| Carat   | Double | Carat weight, Ex: 1.12     |

JSON response:
```
{
    'price_prediction': [predicted price]
}
```

#### (GET) /batch_inference

Parameters:

| Name    | Type   | Description                |
|---------|--------|----------------------------|
| batch   | array  | List of diamond objects containing all information described in the /single_inference endpoint |

JSON response:
```
{
    'diamond_1': {
        'details': {...},
        'price_prediction': [predicted price]
    },
    ...
}
```

#### (POST) /train_model

Parameters: **None**

Response: ```{'success': [True or False]}```

## Prerequisites
#### For training the model
- A database of diamond sales saved as **database.csv** in ```./data/```, preferrably  at least 10'000 sales. For structure, see example in **scraper.py**.

- ```Tensorflow Keras```, ```sklearn```, ```flask``` packages installed

#### For inferring diamond prices

- **regression_estimator.h5** in ```./model/```. This is exported automatically when training the model.

## How to run locally
- Clone the repo
- Run **main.py**
- Send requests to ```localhost:5000``` and enjoy!



## Performance

Model performance is very much dependent on the training data available. I have uploaded a small sample dataset of 20'000 diamond sales which you are welcome to use, but for increased performance I would recommend scraping your own larger dataset than that.

#### Example
This prediction model was trained on 50'000 sales.

**Request:** GET with payload
```{Shape: "Emerald", Color: "J", Clarity: "VS2", Cut: "Ideal", Carat: "1.5"}```

**Response:** ```{price_prediction: 6865.705}```

**Reality:**

This prediction is within +-1% of the only actual diamond I found with these exact properties!

<img src="./readme_assets/example_diamond_border.png" alt="drawing" width="650"/>

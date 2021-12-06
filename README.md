# Diamond Mate REST backend

Flask REST-Api for getting ML-calculated diamond price predictions based on the provided parameters.

Scrape diamond sales, train a price prediction model, and evaluate pricing on unseen constellations of diamond properties, for example to decide whether you are getting ripped off by your local jeweller!

The value of this program relies on the online consensus that the big online dealers (James allen, Adiamor, etc.) sell way closer to actual market price, and can therefore be a good comparison tool for the inexperienced diamond buyer. *I recommend to exclusively train with and consider GIA certified diamonds for more consistent pricing.*

## Endpoints

#### (GET) /single_inference
Parameters:

| Name                                                                              | Type   | Description                |
|-----------------------------------------------------------------------------------|--------|----------------------------|
| Shape                                                                             | String | Diamond shape, Ex: "Round" |
| Color                                                                             | String | Color grade, Ex: "F"       |
| Clarity                                                                           | String | Clarity, Ex: "VVS1"        |
| Cut                                                                               | String | Cut grade, Ex: "Ideal"     |
| Carat                                                                             | Double | Carat weight, Ex: 1.12     |

Response: ```{'prediction': [predicted price]}```

#### (POST) /train_model

Parameters: **None**

Response: ```{'success': [True or False]}```

## Prerequisites
#### For training the model
- A database of diamond sales saved as **database.csv** in ```./data/```, preferrably scraped. For structure, see example in **scraper.py**.

- ```Tensorflow Keras```, ```sklearn```, ```flask``` packages installed

#### For inferring diamond prices

- **regression_estimator.h5** in ```./model/``` this is exported and saved when training the model.


## Performance

Model performance is clearly dependent on the amount of training data available. I have uploaded a small sample dataset of 20'000 diamond sales which you are welcome to use, but for increased performance I would recommend scraping your own larger dataset than that.

#### Example
This prediction model was trained on 50'000 sales.

**Request:** GET with parameters
```{Shape: "Emerald", Color: "J", Clarity: "VS2", Cut: "Ideal", Carat: "1.5"}```

**Response:** ```{prediction: 6865.705}```

**Reality:**

This prediction is within +-1% of an actual diamond with these exact properties!

<img src="./readme_assets/example_diamond_border.png" alt="drawing" width="650"/>

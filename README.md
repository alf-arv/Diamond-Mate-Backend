# Diamond mate REST backend

description

sales pitch

## Endpoints

#### /single_inference


#### /train_model

## Prerequisites


## Performance

Model performance is clearly dependent on the amount of training data available. I have uploaded a small sample dataset of 20'000 diamond sales which you are welcome to use, but for increased performance I would recommend scraping a larger dataset than that.

#### Example
**request:** GET with parameters
```{Shape: "Emerald", Color: "J", Clarity: "VS2", Cut: "Ideal", Carat: "1.5"}```

**Response:** ```{prediction: 6865.705}```

**Reality:**

<img src="./readme_assets/example_diamond_border.png" alt="drawing" width="650"/>

The prediction is within +-1% of the actual diamond!

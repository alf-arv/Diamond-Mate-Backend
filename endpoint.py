"""
Diamond-mate

Alf-arv, 2021
"""
import sys
import os
import json
from inference import do_inference
from flask import request
from flask import Flask
from model_training import train_regression_estimator
from inference import do_inference

app = Flask(__name__)


@app.route('/single_inference', methods = ['GET'])
def single_inference():
    if(request.method == 'GET'):
        res = do_inference(model_path='model', data={
        "Shape": request.args.get('Shape'),
        "Carat": request.args.get('Carat'),
        "Color": request.args.get('Color'),
        "Clarity": request.args.get('Clarity'),
        "Cut": request.args.get('Cut')
        })

        return json.dumps(str({"result":res[0]}))


@app.route('/train_model', methods = ['POST'])
def train_model():
    if(request.method == 'POST'):
        print("Retraining the model")
        stat = train_regression_estimator(os.path.join('data', 'database.csv'), 'model')
        return json.dumps(str({"status": stat}))

if __name__ == '__main__':
    app.run(threaded=False)

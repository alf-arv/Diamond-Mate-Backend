"""
Diamond-Mate-Backend

Alf-arv, 2021
"""
import sys
import os
import json
from flask import request
from flask import Flask
from model_training import train_regression_estimator
from inference import do_inference, do_batch_inference

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
        return json.dumps(str({"price_prediction":res}))


@app.route('/batch_inference', methods = ['GET'])
def batch_inference():
    if(request.method == 'GET'):
        try:
            batch_length = len(request.args.get('batch'))
        except:
            batch_length = 0

        if batch_length > 0:
            res = do_batch_inference(model_path='model', data={
            "batch": request.args.get('batch')
            })
            return json.dumps(str(res))
        else:
            return json.dumps(str({"error": -1}))


@app.route('/train_model', methods = ['POST'])
def train_model():
    if(request.method == 'POST'):
        stat = train_regression_estimator(os.path.join('data', 'database.csv'), 'model')
        return json.dumps(str({"success": stat}))

if __name__ == '__main__':
    app.run(threaded=False)

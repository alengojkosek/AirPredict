import pickle
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

with open('models/linear_regression_0.2.0.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def api_home():
    return 'api works'

@app.route('/air/predict/', methods=['POST'])
def predict_air():

    post = request.get_json()
    df = pd.DataFrame(post)

    df.interpolate(inplace=True)
    print(df)
    prediction = model.predict(df)

    response = {'prediction': float(prediction[0])}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=44933, debug=True)
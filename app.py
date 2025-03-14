from flask import Flask, request, jsonify, render_template, send_file
import pandas as pd
import os
from model import predict_best_doctors

app = Flask(__name__, template_folder='templates', static_folder='static')
DATA_PATH = "dummy_npi_data.csv"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_time = request.form['time']
        best_doctors = predict_best_doctors(input_time, DATA_PATH)

        if not best_doctors:
            return jsonify({"message": "No doctors found"})

        output_file = "predicted_doctors.csv"
        pd.DataFrame(best_doctors, columns=['NPI']).to_csv(output_file, index=False)
        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

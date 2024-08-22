from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the Excel file once at the start
df = pd.read_excel("data/top_gear_data.xlsx")

@app.route('/calculate_speed', methods=['POST'])
@cross_origin()
def calculate_speed():
    data = request.json

    col_1440 = data.get('Input_speed')
    ratio = data.get('ratio')

    if ratio == 0:
        return jsonify({"error": "Ratio cannot be zero"}), 400

    o_p_speed = col_1440 / ratio
    return jsonify({"o_p_speed": round(o_p_speed, 2)})

@app.route('/filter_data', methods=['POST'])
@cross_origin()
def filter_data():
    data = request.json

    kw = data.get('kw')
    col_1440 = data.get('Input_speed')
    ratio = data.get('ratio')
    o_p_speed = data.get('o_p_speed')
    service_factor = data.get('service_factor')
    mounting_type=data.get('mounting_type')
    Gearbox_status=data.get('Gearbox_status')

    # Filter the dataframe based on the provided inputs
    filtered_df = df[(df['kW'] == kw) &
                     (df[1440] == col_1440) &
                     (df['Ratio'] == ratio) &
                     (np.isclose(df['O/p Speed'], o_p_speed, atol=1e-2))]
    print((kw,col_1440,ratio,o_p_speed,service_factor))

    # Check if the filtered data is not empty
    if not filtered_df.empty:
        # Get the mounting_type and Gearbox_status along with the service factor
        results = filtered_df[service_factor].values.tolist()[0]
        return jsonify({"Model": results,"mounting_type":mounting_type,"Gearbox_status":Gearbox_status})
    else:
        return jsonify({"error": "No matching data found."}), 404



if __name__== '_main_':
    app.run(debug=True)

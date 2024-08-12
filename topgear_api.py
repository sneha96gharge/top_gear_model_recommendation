from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the Excel file once at the start
df = pd.read_excel("data/top_gear_data.xlsx")

@app.route('/get_filtered_data', methods=['POST'])
def get_filtered_data():
    data = request.json
    kw = data.get('kw')
    col_1440 = data.get('col_1440')
    ratio = data.get('ratio')
    o_p_speed = data.get('o_p_speed')
    service_factor=data.get('service_factor')

    # Apply the filters
    filtered_df = df[(df['kW'] == kw) &
                     (df[1440] == col_1440) &
                     (df['Ratio'] == ratio) &
                     (np.isclose(df['O/p Speed'], o_p_speed, atol=1e-2))]

    # Check if the filtered data is not empty
    if not filtered_df.empty:
        # Extract the values from the desired column
        results = filtered_df[service_factor].values.tolist()
    else:
        results = []

    # Return the result as a JSON response
    return jsonify(results)

if __name__ == '__main__':  # Corrected line
    app.run(debug=True)

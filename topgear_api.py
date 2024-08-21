import streamlit as st
import pandas as pd
import numpy as np

# Load the Excel file once at the start
df = pd.read_excel("top_gear_data.xlsx")

# Streamlit app
def main():
    st.title("Filtered Data Viewer")

    # Input fields using Streamlit widgets
    kw = st.number_input('Enter kW:', value=0.0, step=0.1)
    col_1440 = st.number_input('Enter 1440 value:', value=0.0, step=0.1)
    ratio = st.number_input('Enter Ratio:', value=0.0, step=0.1)
    o_p_speed = st.number_input('Enter O/p Speed:', value=0.0, step=0.1)
    service_factor = st.number_input('Enter Service Factor:', value=0.0, step=0.1)

    # Apply the filters when the user clicks the button
    if st.button('Get Model'):
        filtered_df = df[(df['kW'] == kw) &
                         (df[1440] == col_1440) &
                         (df['Ratio'] == ratio) &
                         (np.isclose(df['O/p Speed'], o_p_speed, atol=1e-2))]

        # Check if the filtered data is not empty
        if not filtered_df.empty:
            # Assuming service_factor corresponds to a column name
            if service_factor in filtered_df.columns:
                results = filtered_df[service_factor].values.tolist()
                st.write("Filtered Model:", results)
            else:
                st.write(f"No column found for Service Factor: {service_factor}")
        else:
            st.write("No matching data found.")

if _name_ == '_main_':
    main()

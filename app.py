import streamlit as st
from datetime import datetime
import requests

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''
# date and time
ride_date = st.date_input("Select the date of the ride", datetime.today())
ride_time = st.time_input("Select the time of the ride", datetime.now().time())
pickup_datetime = datetime.combine(ride_date, ride_time)
format_datetime = pickup_datetime.strftime("%Y-%m-%d %H:%M:%S")
format_datetime = format_datetime.replace(" ", "+")

# coordinates
pickup_lon = st.number_input("Enter Pickup longitude")
pickup_lat = st.number_input("Enter Pickup latitude")
dropoff_lon = st.number_input("Enter Dropoff longitude")
dropoff_lat = st.number_input("Enter Dropoff latitude")


# passenger count
passenger_count = st.number_input("Number of Passengers", min_value=1, max_value=10, value=1)

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

#url = 'https://taxifare.lewagon.ai/predict'
url = f"http://taxifare.lewagon.ai/predict?pickup_datetime={format_datetime}&pickup_longitude={pickup_lon}&pickup_latitude={pickup_lat}&dropoff_longitude={dropoff_lon}&dropoff_latitude={dropoff_lat}&passenger_count={passenger_count}"

#if url == 'https://taxifare.lewagon.ai/predict':

#    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# Build the dictionary for the API
api_params = {
    "pickup_datetime": f"{ride_date} {ride_time}",
    "pickup_longitude": pickup_lon,
    "pickup_latitude": pickup_lat,
    "dropoff_longitude": dropoff_lon,
    "dropoff_latitude": dropoff_lat,
    "passenger_count": passenger_count,
}

# Call the API
if st.button("Get Fare Prediction"):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            prediction = response.json()["fare"]
            #st.write(url, response.status_code, prediction)
            st.success(f"Predicted Fare: ${prediction:.2f}")
        else:
            st.error(f"Failed to get prediction. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.error("Could not find the location. Please check the addresses.")

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''

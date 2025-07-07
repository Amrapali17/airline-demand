import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Airline Demand Insights", layout="wide")
st.title("✈️ Airline Demand Insights")
st.write("Analyze airline booking demand using AviationStack API")

API_KEY = "41afca0629c81a6c3b0150df0d27beba"
url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&limit=100"

@st.cache_data
def load_data():

    res = requests.get(url)
    if res.status_code != 200:
        st.error("API request failed.")
        return pd.DataFrame()
    data = res.json().get("data", [])
    df = pd.json_normalize(data)
    return df

df = load_data()
if df.empty:
    st.stop()

st.subheader("✈️ Flight Data Sample")
st.dataframe(df[['airline.name', 'flight.iata', 'departure.airport', 'arrival.airport']].dropna().head(10))

df['route'] = df['departure.airport'] + " ➡ " + df['arrival.airport']

st.subheader("🌍 Top 10 Routes")
routes = df['route'].value_counts().reset_index().head(10)
routes.columns = ['Route', 'Flights']
fig = px.pie(routes, values='Flights', names='Route')
st.plotly_chart(fig)

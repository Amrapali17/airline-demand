import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="My Airline Dashboard", layout="wide")
st.title("✈️ Flight Route Dashboard ")
st.caption("📊 Made by Amrapali Dhobe")

API_KEY = "41afca0629c81a6c3b0150df0d27beba"
url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&flight_status=active&limit=100"

if st.button("🔄 Refresh Now"):
    st.rerun()

def fetch_data():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("data", [])
        return pd.json_normalize(data)
    else:
        return pd.DataFrame()

df = fetch_data()

if df.empty:
    st.warning("No data found. Try again later or check the API.")
    st.stop()

st.subheader("📋 Flight Data Preview")
st.dataframe(df[['airline.name', 'flight.iata', 'departure.airport', 'arrival.airport']].dropna().head(10))

st.subheader("🔍 Filter by Airline")
airlines = df['airline.name'].dropna().unique().tolist()
selected = st.selectbox("Choose an airline", ["All"] + sorted(airlines))

if selected != "All":
    df = df[df['airline.name'] == selected]

df['route'] = df['departure.airport'] + " → " + df['arrival.airport']
routes = df['route'].value_counts().reset_index().head(10)
routes.columns = ['Route', 'Flights']
st.subheader("🌍 Top 10 Flight Routes")
st.plotly_chart(px.pie(routes, names='Route', values='Flights'))

df['departure_time'] = pd.to_datetime(df['departure.scheduled'], errors='coerce')
df['hour'] = df['departure_time'].dt.hour
by_hour = df['hour'].value_counts().sort_index().reset_index()
by_hour.columns = ['Hour', 'Flights']
st.subheader("🕒 Flights by Departure Hour")
st.plotly_chart(px.bar(by_hour, x='Hour', y='Flights'))

st.markdown("✅ Built with 💻 by **Amrapali Dhobe** · July 2025")

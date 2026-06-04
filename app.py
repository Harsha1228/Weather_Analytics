import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from datetime import datetime


# PAGE CONFIG
st.set_page_config(
    page_title="Weather Analytics Dashboard",
    layout="wide"
)


# AUTO REFRESH
st_autorefresh(
    interval=60000,
    key="weather_refresh"
)


# LOAD DATA
@st.cache_data(ttl=60)
def load_data():

    engine = create_engine(
        "postgresql://postgres:{DB_PASSWORD}@localhost:5432/weather_analytics"
    )

    query = """
    SELECT *
    FROM weather_data
    ORDER BY recorded_at
    """

    return pd.read_sql(query, engine)


df = load_data()


# TITLE
st.title("Weather Analytics Dashboard")

st.sidebar.success(
    f"Last Updated: {datetime.now().strftime('%H:%M:%S')}"
)

# EMPTY DATA CHECK
if df.empty:
    st.warning("No weather data available.")
    st.stop()


# CITY FILTER
cities = sorted(df["city"].unique())

selected_city = st.sidebar.selectbox(
    "Select City",
    cities
)

filtered_df = df[
    df["city"] == selected_city
]


# LATEST RECORD
latest = filtered_df.iloc[-1]


# KPI CARDS
st.subheader(f"Current Weather - {selected_city}")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Temperature",
    f"{latest['temperature']:.1f} °C"
)

col2.metric(
    "Humidity",
    f"{latest['humidity']} %"
)

col3.metric(
    "Wind Speed",
    f"{latest['wind_speed']} m/s"
)

col4.metric(
    "Condition",
    latest["weather_condition"]
)


# TEMPERATURE TREND
st.subheader("🌡 Temperature Trend")

fig = px.line(
    filtered_df,
    x="recorded_at",
    y="temperature",
    markers=True,
    title=f"{selected_city} Temperature Trend"
)

st.plotly_chart(fig, use_container_width=True)


# HUMIDITY TREND
st.subheader("💧 Humidity Trend")

fig = px.line(
    filtered_df,
    x="recorded_at",
    y="humidity",
    markers=True,
    title=f"{selected_city} Humidity Trend"
)

st.plotly_chart(fig, use_container_width=True)

# WIND SPEED TREND
st.subheader("🌬 Wind Speed Trend")

fig = px.line(
    filtered_df,
    x="recorded_at",
    y="wind_speed",
    markers=True,
    title=f"{selected_city} Wind Speed Trend"
)

st.plotly_chart(fig, use_container_width=True)


# TEMPERATURE DISTRIBUTION
st.subheader("📊 Temperature Distribution")

fig = px.histogram(
    filtered_df,
    x="temperature",
    nbins=15,
    title=f"{selected_city} Temperature Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# WEATHER CONDITIONS
st.subheader("☁ Weather Conditions")

condition_count = (
    filtered_df["weather_condition"]
    .value_counts()
    .reset_index()
)

condition_count.columns = [
    "Condition",
    "Count"
]

fig = px.pie(
    condition_count,
    names="Condition",
    values="Count",
    title=f"{selected_city} Weather Conditions"
)

st.plotly_chart(fig, use_container_width=True)

# RAW DATA
st.subheader(" Weather History")

st.dataframe(
    filtered_df.sort_values(
        "recorded_at",
        ascending=False
    )
)
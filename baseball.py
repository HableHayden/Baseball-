import streamlit as st
import pandas as pd
import plotly.express as px
from pybaseball import batting_stats

# Fetch data (simplified)
def fetch_data(year=2023):
    return batting_stats(year, qual=100)  # qual=100 filters players with 100+ plate appearances

# Clean data
def clean_data(df):
    if not df.empty:
        df["OPS"] = df["OBP"] + df["SLG"]  # Calculate On-base Plus Slugging
        return df[["Name", "Team", "WAR", "OPS", "HR", "AVG"]]
    return df

# Streamlit UI
st.title(" Baseball Stats Dashboard")
year = st.sidebar.selectbox("Year", [2023, 2022, 2021])

# Fetch and clean data
df = clean_data(fetch_data(year))

# Show data
if not df.empty:
    st.header(f"Top Players in {year}")
    st.dataframe(df.sort_values("WAR", ascending=False).head(10))
    
    st.header("WAR vs OPS")
    fig = px.scatter(df, x="OPS", y="WAR", hover_data=["Name"])
    st.plotly_chart(fig)
else:
    st.error("No data found!")

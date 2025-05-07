# Import necessary libraries
import streamlit as st  # For creating web app interface
import pandas as pd  # For data manipulation
import plotly.express as px  # For interactive visualizations
from pybaseball import batting_stats  # For fetching baseball stats

# DATA FETCHING FUNCTION
def fetch_data(year=2023):
    """Retrieve batting statistics for a given year"""
    # batting_stats() comes from pybaseball library
    # qual=100 filters for players with 100+ plate appearances (removes part-timers)
    return batting_stats(year, qual=100)  

# DATA CLEANING FUNCTION
def clean_data(df):
    """Process raw data into analysis-ready format"""
    if not df.empty:  # Only process if data exists
        # Create OPS metric (On-base Plus Slugging) by adding two columns
        df["OPS"] = df["OBP"] + df["SLG"]  
        
        # Select only these key columns for our dashboard
        return df[["Name", "Team", "WAR", "OPS", "HR", "AVG"]]  
    return df  # Return empty df if no data


# STREAMLIT APP LAYOUT
st.title("⚾ Baseball Stats Dashboard")  # Main title

# Sidebar widget for year selection
# Creates a dropdown to choose between 2021-2023
year = st.sidebar.selectbox("Year", [2023, 2022, 2021])  

# DATA PROCESSING
# 1. Fetch data from pybaseball
# 2. Clean/organize the data
df = clean_data(fetch_data(year))  

# DASHBOARD OUTPUT
if not df.empty:  # Only show if we have data
    # SECTION 1: Top Players Table
    st.header(f"Top Players in {year}")
    # Display top 10 players by WAR (Wins Above Replacement)
    st.dataframe(
        df.sort_values("WAR", ascending=False).head(10)  # Sort by WAR descending
    )
    # SECTION 2: Interactive Scatter Plot
    st.header("WAR vs OPS")
    # Create Plotly scatter plot
    fig = px.scatter(
        df,  # Our cleaned data
        x="OPS",  # X-axis: On-base Plus Slugging
        y="WAR",  # Y-axis: Wins Above Replacement
        hover_data=["Name"]  # Show player names on hover
    )
    
    # Display the plot in Streamlit
    st.plotly_chart(fig)  
    
else:  # Error handling if no data
    st.error("No data found!")  # Shows red error message

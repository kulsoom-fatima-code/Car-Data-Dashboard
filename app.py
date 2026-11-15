
import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(
    page_title="Car Data Dashboard",
    page_icon="🚗",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("car_data.csv")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Convert numeric columns
    numeric_columns = [
        "Year",
        "Engine HP",
        "Engine Cylinders",
        "Number of Doors"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

df = load_data()

# Dashboard title
st.title("🚗 Car Data Analysis Dashboard")
st.write("An interactive dashboard to explore car manufacturers, engine power, and transmission types.")

# Sidebar filters
st.sidebar.header("Filter Cars")

makes = sorted(df["Make"].dropna().unique().tolist())
selected_makes = st.sidebar.multiselect(
    "Select Manufacturer",
    makes
)

transmissions = sorted(df["Transmission Type"].dropna().unique().tolist())
selected_transmissions = st.sidebar.multiselect(
    "Select Transmission",
    transmissions
)

# Apply filters
filtered_df = df.copy()

if selected_makes:
    filtered_df = filtered_df[
        filtered_df["Make"].isin(selected_makes)
    ]

if selected_transmissions:
    filtered_df = filtered_df[
        filtered_df["Transmission Type"].isin(selected_transmissions)
    ]

# Dashboard metrics
st.subheader("Car Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Cars", len(filtered_df))

col2.metric(
    "Manufacturers",
    filtered_df["Make"].nunique()
)

avg_hp = filtered_df["Engine HP"].mean()
col3.metric(
    "Average Horsepower",
    f"{avg_hp:.1f}" if pd.notna(avg_hp) else "N/A"
)

common_transmission = (
    filtered_df["Transmission Type"].mode()
)

col4.metric(
    "Popular Transmission",
    common_transmission.iloc[0]
    if not common_transmission.empty else "N/A"
)

st.divider()

# Chart 1: Top manufacturers
st.subheader("1. Top Car Manufacturers")

make_counts = (
    filtered_df["Make"]
    .value_counts()
    .head(10)
    .reset_index()
)

make_counts.columns = ["Make", "Number of Cars"]

fig1 = px.bar(
    make_counts,
    x="Make",
    y="Number of Cars",
    title="Top 10 Car Manufacturers"
)

st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Cars by year
st.subheader("2. Cars by Year")

year_counts = (
    filtered_df["Year"]
    .value_counts()
    .sort_index()
    .reset_index()
)

year_counts.columns = ["Year", "Number of Cars"]

fig2 = px.line(
    year_counts,
    x="Year",
    y="Number of Cars",
    title="Number of Cars by Year"
)

st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Horsepower distribution
st.subheader("3. Engine Horsepower")

fig3 = px.histogram(
    filtered_df.dropna(subset=["Engine HP"]),
    x="Engine HP",
    title="Distribution of Engine Horsepower"
)

st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Transmission types
st.subheader("4. Transmission Types")

transmission_counts = (
    filtered_df["Transmission Type"]
    .value_counts()
    .reset_index()
)

transmission_counts.columns = [
    "Transmission Type",
    "Number of Cars"
]

fig4 = px.pie(
    transmission_counts,
    names="Transmission Type",
    values="Number of Cars",
    title="Cars by Transmission Type"
)

st.plotly_chart(fig4, use_container_width=True)

# Chart 5: Horsepower by manufacturer
st.subheader("5. Average Horsepower by Manufacturer")

hp_by_make = (
    filtered_df.groupby("Make")["Engine HP"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig5 = px.bar(
    hp_by_make,
    x="Make",
    y="Engine HP",
    title="Top 10 Manufacturers by Average Horsepower"
)

st.plotly_chart(fig5, use_container_width=True)

# Show raw data
st.subheader("Dataset")

if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)

st.success("Car Data Dashboard is ready!")

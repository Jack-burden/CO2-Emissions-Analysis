# =================================
# Load Packages
# =================================

# importing required packages for building streamlit app
import pandas as pd
import streamlit as st
import plotly.express as px

# =================================
# Load Cleaned Data
# =================================

# loading cleaned data 
world_df = pd.read_csv("Data/world_data.csv")
country_df = pd.read_csv("Data/country_data.csv")

# =================================
# Styling for charts
# =================================

def style_fig(fig):

    # normalize title text if it exists, adding capital letter as first letter
    if fig.layout.title and fig.layout.title.text:
        text = fig.layout.title.text.replace("_", " ")
        fig.layout.title.text = text[:1].upper() + text[1:]

    fig.update_layout(
        template="plotly_white",
        font = dict(size = 20, color = "black"),
        margin = dict(l=60, r=40, t=80, b=60),
        height = 600,
        width = None,

        # fixing title styling
        title = dict(
            x=0.5,
            xanchor = "center",
            font = dict(size = 28, family="Arial Black", color = "Black")
        ))

        # Axis styling
    fig.update_xaxes(
        title_font=dict(size=20, color="black"),
        tickfont=dict(size=16, color="black"),
        showgrid=True,
        gridcolor="lightgrey"
    )

    fig.update_yaxes(
        title_font=dict(size=20, color="black"),
        tickfont=dict(size=16, color="black"),
        showgrid=True,
        gridcolor="lightgrey"
    )

    return fig

# =================================
# Create User Interface
# =================================

# configuring page
st.set_page_config(
    page_title="CO2 Emissions Dashboard",
    layout="wide"
)

# creating a title
st.title("CO2 Emissions Analysis")

# information on co2 emissions
st.info("All CO₂ emissions values are measured in million tonnes.")

# creating a sidebar
# adding region selection
region = st.sidebar.multiselect(
    "Region",
    ["World", "Asia", "Africa", "Europe", "North America", "South America", "Oceania"]
)

# getting dataset based on region selection
if "World" in region:
    active_df = world_df
    st.warning("GDP data is not available before 2015")
else:
    active_df = country_df

# adding options for data view
if "World" in region:
    view_level = "World"  # force it
    st.sidebar.write("View: World data")
else:
    view_level = st.sidebar.radio(
        "View",
        ["Country", "Continent"]
    )

chart_type = st.sidebar.selectbox(
    "Chart type",
    ["Scatter", "Bar", "Timeseries", "Map"]
)

years = st.sidebar.multiselect(
    "Years",
    sorted(country_df["Year"].unique())
)

numeric_cols = active_df.select_dtypes(include = "number").columns

if chart_type == "Timeseries":

    st.sidebar.write("X axis is Year")

    y_columns = st.sidebar.multiselect(
        "Y axis",
        numeric_cols
    )

elif chart_type == "Map":
    x_axis = None
    y_axis = st.sidebar.selectbox("Y axis", numeric_cols)

else:
    x_axis = st.sidebar.selectbox("X axis", active_df.columns)
    y_axis = st.sidebar.selectbox("Y axis", numeric_cols)

# ===============================
# Filtering data
# ===============================

# getting filtered data
filtered_df = active_df.copy()

# applying year filter
if years:
    filtered_df = filtered_df[filtered_df["Year"].isin(years)]

# applying region filter
if "World" not in region and region:
    filtered_df = filtered_df[filtered_df['Continent'].isin(region)]

if "Continent" in filtered_df.columns and view_level == "Continent":
    plot_df = (filtered_df.groupby(["Continent", "Year"]).sum(numeric_only=True).reset_index())
else:
    plot_df = filtered_df

# =============================
# Creating plots
# =============================

# creating scatter plot for streamlit

# getting accessible colours
BASE_COLOURS = [
    "#0072B2",  # blue
    "#E69F00",  # orange
    "#009E73",  # green
    "#D55E00",  # red-orange
    "#CC79A7",  # purple
    "#56B4E9",  # light blue
    "#F0E442",  # yellow
    "#4D4D4D",  # grey
]

if chart_type == "Scatter":

    if "World" in region:
        colour = None
    else:
        colour = "Continent"
    
    hover_name = "country" if "country" in plot_df.columns else None
    
    fig = px.scatter(plot_df, 
                     x = x_axis, 
                     y = y_axis, 
                     color = colour,
                     color_discrete_sequence=BASE_COLOURS,
                     hover_name = hover_name,
                     hover_data=[x_axis, y_axis],
                     title=f"{x_axis} vs {y_axis}")
    
    fig.update_traces(marker=dict(symbol="x", size=10))

    fig = style_fig(fig)
    
    st.plotly_chart(fig)

elif chart_type == "Timeseries":

    if not y_columns:
        st.warning("Please select at least one Y variable")

    else:
        long_df = plot_df.melt(id_vars= ["Year"],
                               value_vars=y_columns,
                               var_name="Variable",
                               value_name="Value")
        
        min_year = long_df["Year"].min()
        max_year = long_df["Year"].max()
        
        fig = px.line(long_df,
                      x = "Year",
                      y = "Value",
                      color = "Variable",
                      color_discrete_sequence=BASE_COLOURS,
                      title = f"Trend in {', '.join(y_columns)} from {min_year} to {max_year}")
        
        fig = style_fig(fig)
        
        st.plotly_chart(fig)

elif chart_type == "Map":

    if len(years) != 1:
        st.warning("Please select exactly ONE year to display the map.")
        st.stop()

    year = years[0]

    fig = px.choropleth(plot_df,
                        locations="iso_code",
                        color = y_axis,
                        hover_data=y_axis,
                        color_continuous_scale="YlOrRd",
                        title = f"{y_axis} by Country for {year}")
    
    fig = style_fig(fig)

    fig.update_geos(
    fitbounds="locations",
    visible=False)

    fig.update_layout(
    height=800,
    margin=dict(l=0, r=0, t=50, b=0))


    
    st.plotly_chart(fig)

elif chart_type == "Bar":

    fig = px.bar(plot_df,
                 x=x_axis,
                 y=y_axis,
                 title = f"{y_axis} by {x_axis}")
    
    fig = style_fig(fig)
    
    st.plotly_chart(fig)

else:
    st.warning("Please select a chart type!")


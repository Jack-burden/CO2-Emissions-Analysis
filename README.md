# Data visualisation assignment: CO2 analysis with streamlit 

## Description:

This project is a streamit web application that visualises data around co2 emissions to allow users to explore trends, and find insights by creating interactive charts.

## Features:

- Data cleaning and preprocessing
- Exploratory analysis script
- Interactive streamlit web application
- Interactive plotly visualisations
- Filters for year, area, chart type, and x/y variables

# Setting up the project

## 1.Python Installation:

Ensure python 3.11.0 or higher is installed.

This project was tested using python version 3.11.0


## 2.Create a virtual environment:

To create the virtual environment run the following code in your terminal:

python -m venv venv

To activate the virtual environment make sure to run this code in the terminal

.\.venv\Scripts\activate

## 3.Installing dependencies

After creating the virtual environment in the same terminal run the following command to download all of the necessary packages to run the scripts

pip install -r requirements-dev.txt

## 4.Running the Exploratory Analysis

The exploratory analysis .ipynb is not necessary for running the streamlit app, however to gain more insight into the data and the cleaning and preprocessing undertaken before the development of the streamlit app, the notebook can be sun using the 'Run All' button above the script.

Data is pulled from a local Data/ folder saved in this project space.

## 5.Streamlit Web Application

To run the streamlit web application due to an unability ro connect to GitHub the streamlit file should be run using the following command in the terminal.

streamlit run app.py

This will send you to the web application and allow you to use the interactive analysis dashboard.

There is also a link to the web application in section 9 of the README

## 6. Data set description

The project uses data found in the local Data/ folder

This folder contains 4 dataset, 2 of the datasets labelled owid-co2-data and annual-temperature-anomolies are the datasets required for the analysis.ipynb to clean and preprocess the data ready for the streamlit app. These 2 datasets contain a variety of information on co2 emissions and temperature changes by country for every year from 1965 to 2022.

The other 2 datasets labelled country_data and world_data are the cleaned datasets outputted by the analysis.ipynb that are used for the streamlit app. These datasets contain data regarding co2 and temperature values for each country and for aggregated world values provided by the original datasets.

All data is formed from the first 2 datasets used for the analysis.ipynb and data is collected from 'our world in data'

## 7.Project pipeline

- Data is loaded using pandas
- Data is cleaned and preprocessed in the analysis.ipynb notebook
- Exploratory analysis is performed
- The streamlit application is created using app.py
- Visualisations are rendered in the app using interactive filters

## 8.Requirements

All requirements are located in the requirements-dev.txt file

The requirements.txt file is only necessary for the streamlit app saved in hugging face

## 9. Live Demo


A live version of the streamlit application is available at:

https://huggingface.co/spaces/JackBurden/CO2_emissions_analysis

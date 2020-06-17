import os
import json
import pycountry
import plotly.express as px
import pandas as pd

# Current time for auditable data storing purposes
from datetime import date, datetime
today = date.today()
now = datetime.now()
current_time = now.strftime("%H:%M")
timestamp = str(today) + ' ' + str(current_time)

# Global variables
default_input_path = 'Data/world_data_10-05-2020.json'
default_input_props_path = 'Data/world_data_10-05-2020--list_country_properties.json'
default_output_path = 'Results/countryProfiling/country_pandemic_risk ' + timestamp

class DataProcessor():
    def __init__(self, input_path=default_input_path, output_path=default_output_path, input_props_path=default_input_props_path):
        self.input_path = input_path
        self.output_path = output_path
        self.input_props_path = input_props_path
        self.data = {}
        self.props = {}
        self.risk_levels = {}
        self.risk_df = None

    def read(self):
        try:
            with open(self.input_path) as f:
                data = json.load(f)
            with open(self.input_props_path) as f_props:
                props = json.load(f_props)
        except:
            print('Error occured during Data Retrieval')
            data = {}
            props = {}
        self.data = data
        self.props = props

    def assess_risk(self):
        countries_data = self.data
        properties = self.props
        risk_levels = {}
        for country_name in countries_data:
            country_risk_level = 0
            country_data = countries_data[country_name]
            for prop_name in properties:
                if prop_name in country_data:
                    prop_importance = properties[prop_name]
                    country_prop_value = country_data[prop_name]
                    if prop_importance:
                        if country_prop_value:
                            country_risk_level += prop_importance * country_prop_value
                        else:
                            print(country_name, '-', country_prop_value)
                else:
                    print('MISSING', prop_name, 'for', country_name)
                    break
            country_risk_level = round(country_risk_level)
            risk_levels[country_name] = country_risk_level
        # Sorting risk levels
        risk_levels = {k: v for k, v in sorted(risk_levels.items(), key=lambda item: item[1])}
        self.risk_levels = risk_levels

    def risk_to_df(self):
        risk_levels = self.risk_levels
        risk_levels_matrix = []
        for country_name in risk_levels:
            risk_levels_matrix.append([country_name.replace('_', ' '), risk_levels[country_name]])
        risk_df = pd.DataFrame.from_dict(risk_levels_matrix)
        risk_df.columns = ['Country', 'Pandemic-ready score']
        self.risk_df = risk_df

    def get_country_iso(self):
        risk_df = self.risk_df
        if risk_df.empty:
            print('Error - Make sure to generate a risk level dataframe first !')
            return -1
        list_countries = risk_df['Country'].unique().tolist()
        d_country_code = {}
        for country in list_countries:
            try:
                country_data = pycountry.countries.search_fuzzy(country)
                country_code = country_data[0].alpha_3
                d_country_code.update({country: country_code})
            except:
                print('could not add ISO 3 code for ->', country)
                # If could not find country, make ISO code ' '
                d_country_code.update({country: ' '})

        # Add a iso_alpha column to the dataframe
        for k, v in d_country_code.items():
            risk_df.loc[(risk_df.Country == k), 'iso_alpha'] = v

        self.risk_df = risk_df

    def plot_world_heat_map(self):
        risk_df = self.risk_df
        fig = px.choropleth(data_frame=risk_df,
                            locations="iso_alpha",
                            color="Pandemic-ready score",  # value in column 'Confirmed' determines color
                            hover_name="Country",
                            color_continuous_scale='RdYlGn')  # color scale red, yellow green)

        fig.show()

    def export_data(self, output_format="csv"):
        risk_df = self.risk_df
        if output_format == "excel":
            risk_df.to_excel(self.output_path + '.xlsx')
        else:
            risk_df.to_csv(self.output_path + '.csv', sep=';')

if __name__ == "__main__":

    # Initializing class instance
    countries = DataProcessor()
    # Retrieving data
    countries.read()
    #print(countries.data)
    # Calculating risk factor for each country
    countries.assess_risk()
    print('Pandemic-ready scores by country : \n', countries.risk_levels)
    # Generate the cuntry/risk dataframe
    countries.risk_to_df()
    # Associate to each country it's ISO code
    countries.get_country_iso()
    # Generate a World Map of COVID scores
    countries.plot_world_heat_map()
    # Export data as Excel and CSV files
    countries.export_data(output_format="csv")
    countries.export_data(output_format="excel")
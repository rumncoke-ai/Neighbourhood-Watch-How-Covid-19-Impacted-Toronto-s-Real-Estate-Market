"""Neighbourhood Watch: How Covid-19 Impacted Toronto's Real Estate Market
===============================
This file contains the code that sets up the choropleth maps that visualize the data from before
the covid-19 outbreak

Copyright and Usage Information
===============================

This file is provided solely for the marking purposes of TA's of CSC110 at the
University of Tears St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult TA rules.

This file is Copyright (c) 2021 Minha Faheem, Sohee Goo, Julia Bulat, and Rumaisa Chowdhury.
"""
# Import libraries
import json
from plotly import graph_objects as go
import cluster as c


def open_file(filename: json) -> json:
    """Open the json file"""
    with open(filename) as file:
        reader = json.load(file)
    return reader


TORONTO_NEIGHBOURHOODS = open_file('neighbourhoods.geojson')

# dataframe
_, NON_COVID_DATA = c.main()

# Initialize figure
FIG1 = go.Figure()

# Add Traces
FIG1.add_trace(
    go.Choroplethmapbox(geojson=TORONTO_NEIGHBOURHOODS,  # Assign geojson file
                        featureidkey='properties.AREA_SHORT_CODE',
                        hovertext=NON_COVID_DATA['Neighbourhood Name'],
                        locations=NON_COVID_DATA['Neighbourhood ID'],  # Assign location data,
                        z=NON_COVID_DATA['Cluster Labels'],  # Assign information data
                        colorbar={'title': 'Neighbourhood Desirability Index',
                                  'tickmode': 'array', 'nticks': 3, 'tickvals': [0, 1, 2],
                                  'ticktext': ['Least Desirable', 'Semi-Desirable',
                                               'Most Desirable']},
                        colorscale='Burg',
                        zauto=True,
                        showscale=True
                        ))

FIG1.add_trace(
    go.Choroplethmapbox(geojson=TORONTO_NEIGHBOURHOODS,  # Assign geojson file
                        featureidkey='properties.AREA_SHORT_CODE',
                        hovertext=NON_COVID_DATA['Neighbourhood Name'],
                        locations=NON_COVID_DATA['Neighbourhood ID'],  # Assign location data,
                        z=NON_COVID_DATA['Avg Crime Rate'],  # Assign information data
                        colorscale='Purpor',
                        colorbar={'title': 'Crime Rate (per 100,000 people)'},
                        zauto=True,
                        showscale=True
                        ))
FIG1.add_trace(
    go.Choroplethmapbox(geojson=TORONTO_NEIGHBOURHOODS,  # Assign geojson file
                        featureidkey='properties.AREA_SHORT_CODE',
                        hovertext=NON_COVID_DATA['Neighbourhood Name'],
                        locations=NON_COVID_DATA['Neighbourhood ID'],  # Assign location data,
                        z=NON_COVID_DATA['Avg Property Price'],  # Assign information data
                        colorscale='tealrose',
                        colorbar={'title': 'Average Property Price (in millions)'},
                        zauto=True,
                        showscale=True
                        ))


# Display Configurations
FIG1.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="Desirability Index",
                     method="update",
                     args=[{"visible": [True, False, False]},
                           {"title": "Toronto Neighbourhoods Desirability Index Before Covid"}]),
                dict(label="Crime Rate",
                     method="update",
                     args=[{"visible": [False, True, False]},
                           {"title": "Crime Rate in Toronto Neighbourhoods Before Covid"}]),
                dict(label="Property Prices",
                     method="update",
                     args=[{"visible": [False, False, True]},
                           {"title": "Average Property Prices in "
                                     "Toronto Neighbourhood Before Covid"}]),
            ]),
        )
    ])

# Update layout
FIG1.update_layout(

    mapbox_style="carto-positron",  # Decide a style for the map
    mapbox_zoom=9,  # Zoom in scale
    mapbox_center={"lat": 43.7, "lon": -79.4},  # Center location of the map
)

if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['json', 'plotly', 'cluster'],
        'allowed-io': ['open_file'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

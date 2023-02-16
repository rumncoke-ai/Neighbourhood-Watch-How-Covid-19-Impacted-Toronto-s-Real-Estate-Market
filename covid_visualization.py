"""Neighbourhood Watch: How Covid-19 Impacted Toronto's Real Estate Market
===============================
This file contains the code that sets up the choropleth maps that visualize the data from after
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
COVID_DATA, _ = c.main()

# Initialize figure
FIG = go.Figure()

# Create figure object
# Add Traces

FIG.add_trace(
    go.Choroplethmapbox(geojson=TORONTO_NEIGHBOURHOODS,  # Assign geojson file
                        featureidkey='properties.AREA_SHORT_CODE',
                        hovertext=COVID_DATA['Neighbourhood Name'],
                        locations=COVID_DATA['Neighbourhood ID'],  # Assign location data,
                        z=COVID_DATA['Cluster Labels'],  # Assign information data
                        colorscale='Burg',
                        colorbar={'title': 'Neighbourhood Desirability Index',
                                  'tickmode': 'array',
                                  'nticks': 3,
                                  'tickvals': [0, 1, 2],
                                  'ticktext': ['Least Desirable', 'Semi-Desirable',
                                               'Most Desirable']},
                        zauto=True,
                        showscale=True

                        ))


FIG.add_trace(
    go.Choroplethmapbox(geojson=TORONTO_NEIGHBOURHOODS,  # Assign geojson file
                        featureidkey='properties.AREA_SHORT_CODE',
                        locations=COVID_DATA['Neighbourhood ID'],  # Assign location data
                        z=COVID_DATA['Avg Vaccination Rate'],  # Assign information data
                        zauto=True,
                        hovertext=COVID_DATA['Neighbourhood Name'],
                        colorscale='viridis',
                        colorbar={'title': 'Average Vaccination Rate (Percentage)'},
                        showscale=True
                        ))
FIG.add_trace(
    go.Choroplethmapbox(geojson=TORONTO_NEIGHBOURHOODS,  # Assign geojson file
                        featureidkey='properties.AREA_SHORT_CODE',
                        hovertext=COVID_DATA['Neighbourhood Name'],
                        locations=COVID_DATA['Neighbourhood ID'],  # Assign location data,
                        z=COVID_DATA['Avg Covid Case Rate'],  # Assign information data
                        zauto=True,
                        colorscale='Blues',
                        colorbar={'title': 'Average Covid Case Rate (per 100,000 people)'},
                        showscale=True
                        ))

FIG.add_trace(
    go.Choroplethmapbox(geojson=TORONTO_NEIGHBOURHOODS,  # Assign geojson file
                        featureidkey='properties.AREA_SHORT_CODE',
                        hovertext=COVID_DATA['Neighbourhood Name'],
                        locations=COVID_DATA['Neighbourhood ID'],  # Assign location data,
                        z=COVID_DATA['Avg Unemployment Rate'],  # Assign information data
                        zauto=True,
                        colorscale='darkmint',
                        colorbar={'title': 'Average Unemployment Rate (Percentage)'},
                        showscale=True
                        ))
FIG.add_trace(
    go.Choroplethmapbox(geojson=TORONTO_NEIGHBOURHOODS,  # Assign geojson file
                        featureidkey='properties.AREA_SHORT_CODE',
                        hovertext=COVID_DATA['Neighbourhood Name'],
                        locations=COVID_DATA['Neighbourhood ID'],  # Assign location data,
                        z=COVID_DATA['Avg Property Price'],  # Assign information data
                        zauto=True,
                        colorscale='tealrose',
                        colorbar={'title': 'Average Property Price (in millions)'},
                        showscale=True
                        ))

FIG.add_trace(
    go.Choroplethmapbox(geojson=TORONTO_NEIGHBOURHOODS,  # Assign geojson file
                        featureidkey='properties.AREA_SHORT_CODE',
                        hovertext=COVID_DATA['Neighbourhood Name'],
                        locations=COVID_DATA['Neighbourhood ID'],  # Assign location data,
                        z=COVID_DATA['Avg Crime Rate'],  # Assign information data
                        zauto=True,
                        colorscale='Purpor',
                        colorbar={'title': 'Average Crime Rate (per 100,000 people)'},
                        showscale=True
                        ))


FIG.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="Desirability Index",
                     method="update",
                     args=[{"visible": [True, False, False, False, False, False]},
                           {"title": "Toronto Neighbourhoods Desirability Index"}]),
                dict(label="Vaccination Rate",
                     method="update",
                     args=[{"visible": [False, True, False, False, False, False]},
                           {"title": "Vaccination Completion in Toronto Neighbourhoods"}]),
                dict(label="Covid-19 Rate",
                     method="update",
                     args=[{"visible": [False, False, True, False, False, False]},
                           {"title": "Covid-19 in Toronto Neighbourhoods (per 100,000 people)"}]),
                dict(label="Unemployment Rate",
                     method="update",
                     args=[{"visible": [False, False, False, True, False, False]},
                           {"title": "Unemployment Rate in Toronto Neighbourhoods"}]),
                dict(label="Property Prices",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, False]},
                           {"title": "Average Property Prices in Toronto Neighbourhood"}]),
                dict(label="Crime Rate",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, True]},
                           {"title": "Crime Rate in Toronto Neighbourhoods"}]),
            ]),
        )
    ])

# Update layout
FIG.update_layout(

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

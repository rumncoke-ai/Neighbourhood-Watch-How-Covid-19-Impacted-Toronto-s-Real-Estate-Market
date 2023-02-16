"""Neighbourhood Watch: How Covid-19 Impacted Toronto's Real Estate Market

===============================
This file contains the data processing functions and the main clustering functions

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
import csv
import pandas as pd
from sklearn.cluster import KMeans
from kneed import KneeLocator


def main() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Returns a tuple with two dataframes after compiling data sets together then computes
    clustering on them.

    The first dataframe contains data that is post-covid. The second dataframe contains data
    that is pre-covid
    """

    # Converts all files into lists of lists.
    a = convert_file("neighbourhood_cases.csv")
    b = convert_file("neighbourhood_census.csv")
    c = convert_file("neighbourhood_crime_rates.csv")
    d = convert_file("property_prices.csv")
    e = convert_file("vaccine_trends.csv")

    # Provides us with lists of lists of all data, including covid (covid rates, vaccination
    # rates, etc.) and lists of lists of data from all data minus the covid data.
    covid_data, non_covid_data = combine_datasets(d, e, a, c, b)

    # Convert both covid_data and non_covid_data into dataframes.
    covid_data = convert_to_dataframe(covid_data)
    non_covid_data = convert_to_dataframe(non_covid_data)

    # Clean up both datasets (basically just add column names).
    cluster_data1, cluster_data2 = cleanup_data(covid_data, non_covid_data)

    # Determine the optimal number of clusters for both data sets.
    num_of_clusters1 = elbow_method(cluster_data1)
    num_of_clusters2 = elbow_method(cluster_data2)

    c_data = determine_neighbourhood_appeal(cluster_data1, num_of_clusters1)
    non_c_data = determine_neighbourhood_appeal(cluster_data2, num_of_clusters2)

    return (c_data, non_c_data)


def determine_neighbourhood_appeal(cluster_data: pd.DataFrame, kclusters: int) -> pd.DataFrame:
    """Return the mean values in the dataset, grouped into kclusters number of clusters."""

    clustering = cluster_data.copy()

    # remove the non-numerical data for the dataframe
    clustering.drop(labels=['Neighbourhood ID', 'Neighbourhood Name'], axis=1, inplace=True)

    # fits the data to the model with the optimal number of clusters.
    kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(clustering)

    # Insert a column into the dataset that tells us which cluster each neighbourhood belongs in.
    cluster_data.insert(0, 'Cluster Labels', kmeans.labels_)

    cluster_data['Cluster Labels'] = cluster_data['Cluster Labels'].replace([0, 1, 2], [2, 0, 1])

    return cluster_data


def elbow_method(data: pd.DataFrame) -> int:
    """Return the optimal number of clusters for the given dataset."""

    # make a copy of the pandas dataframe for clustering
    clustering = data.copy()
    # remove the non-numerical data for the dataframe
    clustering.drop(labels=['Neighbourhood ID', 'Neighbourhood Name'], axis=1, inplace=True)

    # make an empty list to keep track of all inertias
    inertia_list = []

    k_value = range(1, 10)
    # iterate through each number from 0 to 9 inclusive to find the best k value for our data
    for k in k_value:
        # initialize the model and set k to be the number of clusters
        kmean_model = KMeans(n_clusters=k)

        # fits the data to the model with k clusters
        kmean_model.fit(clustering)

        # the inertia_ method measures the sum of squared distances of samples to their
        # closest cluster center. a smaller inertia_ is aimed for so that the center of
        # the cluster
        # is in the right position.
        inertia_list.append(kmean_model.inertia_)

    # the KneeLocator class locates the optimum number of clusters.
    # too little clusters cause some disjoint groups of data are forced to fit into one larger
    # cluster.
    # while too many clusters creates artificial boundaries within real data clusters.
    knee_locator = KneeLocator(range(1, 10), inertia_list, curve="convex", direction="decreasing")

    return int(knee_locator.elbow)


def combine_datasets(property_prices: list[list],
                     vaccine_trends: list[list],
                     covid_cases: list[list],
                     crime_rates: list[list],
                     unemployment: list[list]) -> (list[list], list[list]):
    """Return the combination of the information from 3 datasets as a single list of lists."""
    temp_lst1 = []
    temp_lst2 = []
    covid_dataset = []
    not_covid_dataset = []

    for i in range(len(property_prices)):
        if i != 0:
            temp_lst1.append(property_prices[i][0])
            temp_lst1.append(property_prices[i][1])
            temp_lst1.append(average_house_price(property_prices, property_prices[i][1]))
            temp_lst1.append(average_vaccination_rate(vaccine_trends, vaccine_trends[i][1]))
            temp_lst1.append(average_covid_cases_rate(covid_cases, covid_cases[i][1]))
            temp_lst1.append(average_unemployment_rate(unemployment, unemployment[i][1]))
            temp_lst1.append(average_crime_rate(crime_rates, crime_rates[i][1]))

            temp_lst2.append(property_prices[i][0])
            temp_lst2.append(property_prices[i][1])
            temp_lst2.append(average_house_price_pre_covid(property_prices, property_prices[i][1]))
            temp_lst2.append(average_unemployment_rate(unemployment, unemployment[i][1]))
            temp_lst2.append(average_crime_rate_pre_covid(crime_rates, crime_rates[i][1]))

            covid_dataset.append(temp_lst1)
            not_covid_dataset.append(temp_lst2)

        temp_lst1 = []
        temp_lst2 = []
    return covid_dataset, not_covid_dataset


def convert_to_dataframe(data: list[list]) -> pd.DataFrame:
    """Convert data into a dataframe using the Pandas library."""

    dataframe = pd.DataFrame(data)
    return dataframe


def cleanup_data(data1: pd.DataFrame, data2: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return dataframes that have accurate columns."""

    data1.columns = ['Neighbourhood ID', 'Neighbourhood Name', 'Avg Property Price',
                     'Avg Vaccination Rate', 'Avg Covid Case Rate', 'Avg Unemployment Rate',
                     'Avg Crime Rate']
    data2.columns = ['Neighbourhood ID', 'Neighbourhood Name', 'Avg Property Price',
                     'Avg Unemployment Rate', 'Avg Crime Rate']
    return data1, data2


def convert_file(filename: str) -> list[list]:
    """Return the given csv file as a list of lists."""
    with open(filename) as file:
        reader = csv.reader(file)

        # Make data into a list of lists
        data_so_far = []

        for row in reader:
            temp_row = [row[item] for item in range(len(row))]
            data_so_far.append(temp_row)
        return data_so_far


def average_covid_cases_rate(data: list[list], neighbourhood: str) -> float:
    """Return the average covid case rate of the given city from 2020 to 2021"""

    for i in range(len(data)):
        if data[i][1] == neighbourhood:
            case_rate = float(str.strip(data[i][2]))
            return case_rate
    return 0.0


def average_vaccination_rate(data: list[list], neighbourhood: str) -> float:
    """Return the average vaccination rate of the given city from 2020 to 2021."""

    for i in range(len(data)):
        if data[i][1] == neighbourhood:
            vax_rate = float((str.strip(data[i][4])))
            return vax_rate
    return 0.0


def average_house_price(data: list[list], neighbourhood: str) -> float:
    """Return the average house price index of the given city from 2020 to 2021."""

    # find the average house price index for each city from 2020 - 2021.
    for i in range(len(data)):
        if data[i][1] == neighbourhood:
            house_price = float(str.strip(data[i][2])) + float(str.strip(data[i][3]))
            return house_price / 2
    return 0.0


def average_house_price_pre_covid(data: list[list], neighbourhood: str) -> float:
    """Return the average house price index of the given city from 2020 to 2021."""

    # find the average house price index for each city from 2020 - 2021.
    for i in range(len(data)):
        if data[i][1] == neighbourhood:
            house_price = float(str.strip(data[i][4]))
            return house_price

    return 0.0


def average_unemployment_rate(data: list[list], neighbourhood: str) -> float:
    """Return the average house price index of the given city from 2020 to 2021."""

    # find the average house price index for each city from 2020 - 2021.
    for i in range(len(data)):
        if data[i][1] == neighbourhood:
            unemployment = float(str.strip(data[i][2]))
            return unemployment
    return 0.0


def average_crime_rate(data: list[list], neighbourhood: str) -> float:
    """Return the average house price index of the given city from 2020 to 2021."""

    # find the average house price index for each city from 2020 - 2021.
    for i in range(len(data)):
        if data[i][1] == neighbourhood:
            crime_rate = float(str.strip(data[i][4]))
            return crime_rate
    return 0.0


def average_crime_rate_pre_covid(data: list[list], neighbourhood: str) -> float:
    """Return the average house price index of the given city from 2018 to 2019."""

    # find the average house price index for each city from 2018 to 2019..
    for i in range(len(data)):
        if data[i][1] == neighbourhood:
            crime_rate = float(str.strip(data[i][2]))
            return crime_rate
    return 0.0


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pandas', 'csv', 'sklearn.cluster', 'kneed'],
        'allowed-io': ['convert_to_dataframe', 'convert_file'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

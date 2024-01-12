import pandas as pd
import numpy as np
import geopandas as gpd


class ConnectionScorer:
    def __init__(self):
        pass

    def calculate_proximity_score(self, stork_a: pd.DataFrame, stork_b: pd.DataFrame) -> dict:
        """
        Calculates proximity score between two storks.
        :param stork_a: Stork A dataframe
        :param stork_b: Stork B dataframe
        :return: Proximity score
        """
        stork_a_points = stork_a[["location-lat", "location-long"]].values
        stork_b_points = stork_b[["location-lat", "location-long"]].values

        return {}

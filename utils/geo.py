import geopy
import geopy.distance
import pandas as pd
import numpy as np


def wgs84_to_web_mercator(df: pd.DataFrame, lon: str = "location-long", lat: str = "location-lat") -> pd.DataFrame:
    """
    Maps WGS84 coordinates to Web Mercator.
    https://en.wikipedia.org/wiki/Web_Mercator_projection
    :param df: Dataframe with coordinates
    :param lon: Name of longitude column
    :param lat: Name of latitude column
    :return:
    """
    k = 6378137  # Earth radius in meters
    df["x"] = df[lon] * (k * np.pi / 180.0)
    df["y"] = np.log(np.tan((90 + df[lat]) * np.pi / 360.0)) * k

    return df


def distance_wgs84(lat_a: float, long_a: float, lat_b: float, long_b: float) -> float:
    """
    Calculates distance between two points in WGS84 coordinate system in meters.
    :return: Distance in meters
    """
    coords_1 = (lat_a, long_a)
    coords_2 = (lat_b, long_b)

    return geopy.distance.geodesic(coords_1, coords_2).m


def distance_web_mercator(x_a: float, y_a: float, x_b: float, y_b: float) -> float:
    """
    Calculates distance between two points in Web Mercator coordinate system in meters.
    :return: Distance in meters
    """

    return np.sqrt((x_b - x_a) ** 2 + (y_b - y_a) ** 2)

import pandas as pd
import osmnx as ox
from datetime import datetime

from osmnx._errors import InsufficientResponseError

# # mapping all possible landuse values to developed land, green_land (forests, grass, meadow), rural, water
landuse_dict = {
    'residential': 'developed_land',
    'industrial': 'developed_land',
    'cemetery': 'developed_land',
    'commercial': 'developed_land',
    'fairground': 'developed_land',
    'institutional': 'developed_land',
    'retail': 'developed_land',
    'quarry': 'developed_land',
    'construction': 'developed_land',
    'recreation_ground': 'developed_land',
    'brownfield': 'developed_land',
    'religious': 'developed_land',
    'garages': 'developed_land',
    'military': 'developed_land',
    'railway': 'developed_land',
    'greenfield': 'developed_land',
    'landfill': 'developed_land',
    'highway': 'developed_land',
    'education': 'developed_land',
    'static_caravan': 'developed_land',
    'winter_sports': 'developed_land',
    'depot': 'developed_land',

    'farmland': 'rural',
    'orchard': 'rural',
    'farmyard': 'rural',
    'vineyard': 'rural',
    'allotments': 'rural',
    'village_green': 'rural',
    'greenhouse_horticulture': 'rural',
    'logging': 'rural',
    'paddy': 'rural',
    'animal_keeping': 'rural',
    'farm': 'rural',

    'grass': 'green_land',
    'forest': 'green_land',
    'meadow': 'green_land',
    'plant_nursery': 'green_land',
    'flowerbed': 'green_land',
    'greenery': 'green_land',

    'basin': 'water',
    'reservoir': 'water',
    'aquaculture': 'water',
    'salt_pond': 'water',
}

tags = {
    'landuse': True
}


def get_landuse(lat, long):
    try:
        df = ox.features_from_point(center_point=(lat, long), tags=tags, dist=2000)
    except InsufficientResponseError:
        return 'other'
    landuse_val = df['landuse'].mode()[0]
    mapped = landuse_dict.get(landuse_val)
    if mapped is not None:
        return mapped
    else:
        return 'other'


data = pd.read_csv('afr_pl_2_cleaned_v2.csv')
data = data.drop(['Unnamed: 0'], axis=1)
data = data.reset_index(drop=True)
data['area_type'] = None

# data = data.assign(area_type=lambda row: (get_landuse(row['location-lat'], row['location-long'])))

for idx, row in data.iterrows():
    data.at[idx, 'area_type'] = get_landuse(row['location-lat'], row['location-long'])
    if idx % 100 == 0 and idx != 0:
        print(len(data.index) - idx, 'left...')

data.to_csv('afr_pl_2_cleaned_v3.csv')

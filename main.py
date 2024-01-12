import pandas as pd
import numpy as np
import geopy.distance
from datetime import datetime
from utils.computation import ConnectionScorer

FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class StorkData:
    def __init__(self, stork_id, all_occurrences):
        self.stork_id = stork_id
        self.all_occurrences = all_occurrences

    def count_score(self, otherStork):
        total_score = 0.0
        for stork_a_idx in range(len(self.all_occurrences.index)):
            stork_a = self.all_occurrences.iloc[[stork_a_idx]]
            # if stork_a_idx % 10 == 0 and stork_a_idx != 0:
            #     print(datetime.now(), len(self.all_occurrences.index) - stork_a_idx, ' left...')
            #     print(total_score)
            for stork_b_idx in range(len(otherStork.all_occurrences.index)):
                stork_b = otherStork.all_occurrences.iloc[[stork_b_idx]]
                dist = count_distance(stork_a['location-lat'][stork_a_idx], stork_a['location-long'][stork_a_idx], stork_b['location-lat'][stork_b_idx], stork_b['location-long'][stork_b_idx])
                time_diff = count_time_diff(stork_a['date'][stork_a_idx], stork_b['date'][stork_b_idx])
                total_score += score_value(dist, time_diff)
        return total_score, total_score / len(self.all_occurrences.index)


def score_value(dist, time_diff, max_dist=1, max_time_diff=3600, weight=1):
    if dist > max_dist or time_diff > max_time_diff:
        return 0
    return (float(max_dist) / (dist+0.0000001) + float(max_time_diff) / (time_diff+0.0000001)) * weight


# return distance between two geo points in km
def count_distance(lat_a, long_a, lat_b, long_b):
    return geopy.distance.geodesic((lat_a, long_a), (lat_b, long_b)).km


# returns time difference in seconds between two string dates
def count_time_diff(datetime_a, datetime_b):
    dt_a = datetime.strptime(datetime_a, FORMAT)
    dt_b = datetime.strptime(datetime_b, FORMAT)
    return abs((dt_a - dt_b).total_seconds())


if __name__ == "__main__":
    data = pd.read_csv('data/stroke_migration/LifeTrack_white_stork_clean.csv')
    # occ_data = pd.read_csv('occurences.csv')
    # unique_ids = occ_data['stork_id']

    a_data = data.loc[data['tag-local-identifier'] == 4571]
    a_data = a_data.reset_index(drop=True)

    b_data = data.loc[data['tag-local-identifier'] == 4554]
    b_data = b_data.reset_index(drop=True)

    start = datetime.now()
    print('Start time: ', start)

    cs = ConnectionScorer()
    score = cs.calculate_proximity_score(a_data, b_data)
    print(score)

    end = datetime.now()
    print('End time: ', end)
    print('Finished after', end - start)

    # s_a = StorkData(4571, a_data)
    # s_b = StorkData(4554, b_data)
    # start = datetime.now()
    # print('Start time: ', start)
    # total_score, mean_score = s_a.count_score(s_b)
    # print('Total score: ', total_score, '\nMean score: ', mean_score)
    # end = datetime.now()
    # print('End time: ', end)
    # print('Finished after', end - start)


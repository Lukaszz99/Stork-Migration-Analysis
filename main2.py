import pandas as pd
import numpy as np
import geopy.distance
from datetime import datetime
from utils.computation import ConnectionScorer

if __name__ == "__main__":
    df = pd.read_csv("data/stroke_migration/pl_afr_3_filtered.csv")

    stork_1 = df.loc[df['stork_migration_id'] == "3955_pl_afr_3"]
    stork_1 = stork_1.reset_index(drop=True)

    stork_2 = df.loc[df['stork_migration_id'] == "3950_pl_afr_3"]
    stork_2 = stork_2.reset_index(drop=True)

    start = datetime.now()
    print('Start time: ', start)

    cs = ConnectionScorer(distance_threshold=20000.0, time_threshold=720.0)  # 20km and 12h
    score = cs.calculate_proximity_score(stork_1, stork_2)
    print(score)

    end = datetime.now()
    print('End time: ', end)
    print('Finished after', end - start)
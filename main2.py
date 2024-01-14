import pandas as pd
import numpy as np
import geopy.distance
from datetime import datetime
from utils.computation import ConnectionScorer


def append_score(filename: str, pair: str, score: float):
    with open(filename, 'a') as f:
        f.write(f"{pair[0]}\t{pair[1]}\t{score}\n")


if __name__ == "__main__":
    start = datetime.now()
    print('Start time: ', start)

    df = pd.read_csv("data/stroke_migration/pl_afr_3_cleaned_v2.csv")

    unique_ids = df['stork_migration_id'].unique()

    id_pais = [(a, b) for idx, a in enumerate(unique_ids) for b in unique_ids[idx + 1:]]
    print(f"#Pairs: {len(id_pais)}")
    print(f"All pairs: {id_pais}")

    for i, pair in enumerate(id_pais):
        print(f"Current pair: {pair}\t{i + 1}/{len(id_pais)}\n")

        stork_1 = df.loc[df['stork_migration_id'] == pair[0]]
        stork_1 = stork_1.reset_index(drop=True)

        stork_2 = df.loc[df['stork_migration_id'] == pair[1]]
        stork_2 = stork_2.reset_index(drop=True)

        cs = ConnectionScorer(distance_threshold=50000.0, time_threshold=10080.0)  # 50km and 7 days
        score = cs.calculate_proximity_score(stork_1, stork_2)
        print(f"Pair {pair} score: {score}\n")

        append_score("pl_afr_3_scores.txt", pair, score)

    end = datetime.now()
    print('End time: ', end)
    print('Finished after', end - start)

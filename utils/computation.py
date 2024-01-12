import pandas as pd
import geopy.distance


class ConnectionScorer:
    def __init__(self, distance_threshold: float = 1000.0, time_threshold: float = 180.0):
        """

        :param distance_threshold: Distance threshold in meters
        :param time_threshold: Time threshold in minutes
        """
        self.distance_threshold = distance_threshold
        self.time_threshold = time_threshold

    def calculate_proximity_score(self, stork_a: pd.DataFrame, stork_b: pd.DataFrame) -> float:
        """
        Calculates proximity score between two storks.
        :param stork_a: Stork A dataframe
        :param stork_b: Stork B dataframe
        :return: Proximity score
        """
        stork_a_points = stork_a[["location-lat", "location-long", "timestamp"]].values
        stork_b_points = stork_b[["location-lat", "location-long", "timestamp"]].values

        total_score = 0.0

        total_iterations = len(stork_a_points) * len(stork_b_points)
        print(f"Total iterations: {total_iterations}")
        it = 0
        for stork_a_pt in stork_a_points:
            for stork_b_pt in stork_b_points:
                it += 1
                if it % 10000 == 0:
                    print(f"Iteration: {it}/{total_iterations}\t {(it / total_iterations) * 100}%")

                time_diff = self._calculate_timedelta(stork_a_pt[2], stork_b_pt[2])

                # if storks were more that threshold time apart, skip
                if time_diff > self.time_threshold:
                    continue

                distance_diff = self._calculate_distance(stork_a_pt[:2], stork_b_pt[:2])

                # if storks were more that threshold distance apart, skip
                if distance_diff > self.distance_threshold:
                    continue

                tmp_score = self._calculate_score(distance_diff, time_diff, weight=1.0)
                total_score += tmp_score

        return total_score

    def _calculate_score(self, distance_diff: float, time_diff: float, weight: float = 1.0) -> float:
        return (self.distance_threshold / distance_diff + self.time_threshold / time_diff) * weight

    def _calculate_timedelta(self, time_a: str, time_b: str):
        return max(1,
                   (pd.Timestamp(time_a) - pd.Timestamp(time_b)).total_seconds() / 60)

    def _calculate_distance(self, pt_a, pt_b):
        """
        Calculates distance between two points in meters. Returns at least 5 meters, to avoid division by small values
        :param pt_a:
        :param pt_b:
        :return:
        """
        dst = geopy.distance.geodesic(pt_a, pt_b).m
        return max(5, dst)

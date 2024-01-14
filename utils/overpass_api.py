import requests
import json


class OverpassAPI:
    def __init__(self, overpass_url: str ="http://overpass-api.de/api/interpreter"):
        self._url = overpass_url

    def execute_query(self, query: str):
        response = requests.get(self._url,
                                params={'data': query})
        data = response.json()

        return data


if __name__ == '__main__':
    query = """
            [out:json];
            area["ISO3166-1"="PL"][admin_level=2];
            (way["boundary"="forest"](area);
            );
            out meta;
            """

    overpass = OverpassAPI()
    data = overpass.execute_query(query=query)
    print(data["elements"])

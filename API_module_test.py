import time
import requests
import json
import os

lokalizacja = os.getenv("locations", "Warszawa")

class WeatherRequester:
    def __init__(self, lokalizacja):
        self.lokalizacja = lokalizacja
        self.api_url = "https://api.openaq.org/v2/locations"
        self.headers = {
            "X-API-Key": "f683e5cd6415f93685ef1d57d765e2ebd97565439364607016c1176274700db7"
        }

    def loop(self):
        while True:
            try:
                response = requests.get(self.api_url, headers=self.headers, params={"city": self.lokalizacja, "limit": 1})
                # Sprawdzanie kodu odpowiedzi
                if response.status_code != 200:
                    raise Exception("Error: Received status code {response.status_code}")
                data = response.json()
                if (len(data["results"]) == 0):
                    raise Exception("Nie ma wynikow")
                    # Tworzenie struktury JSON zgodnej z wymaganiami
                msg = {
                    "location": self.lokalizacja,
                    "timestamp": data["results"][0]["lastUpdated"],
                    "values": [
                        {param["parameter"]: param["lastValue"]}
                        for param in data["results"][0]["parameters"]
                    ]
                }
                print(json.dumps(msg, indent=4))
            except Exception as e:
                print(f"An error occurred: {e}")

            # Opóźnienie 30 sekund przed kolejnym żądaniem
            time.sleep(30)



weather_requester = WeatherRequester("Warszawa")
weather_requester.loop()
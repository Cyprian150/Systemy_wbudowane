import time
import requests
import json
import os
import paho.mqtt.publish as publish

class WeatherRequester:
    def __init__(self, lokalizacja, mqtt_host_name, mqtt_topic):
        self.lokalizacja = lokalizacja
        self.api_url = "https://api.openaq.org/v2/locations"
        self.headers = {
            "X-API-Key": "f683e5cd6415f93685ef1d57d765e2ebd97565439364607016c1176274700db7"
        }

        #publisher
        self.host_name = mqtt_host_name
        self.topic = mqtt_topic
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
                print("host_name:")
                print(mqtt_host_name)
                print(json.dumps(msg, indent=4))
                publish.single(topic = self.topic, payload = json.dumps(msg), hostname = self.host_name)

            except Exception as e:
                print(f"An error occurred: {e}")
            # Opóźnienie 30 sekund przed kolejnym żądaniem
            time.sleep(30)

if __name__ == '__main__':
    lokalizacja = os.getenv("locations", "Warszawa")
    mqtt_host_name = os.getenv("mqtt_host_name", "localhost")
    mqtt_topic = os.getenv("mqtt_topic", "AirQuality")
    weather_requester = WeatherRequester(lokalizacja, mqtt_host_name, mqtt_topic)
    weather_requester.loop()
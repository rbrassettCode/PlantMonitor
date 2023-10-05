import RPi.GPIO as GPIO
import time
import requests


URL = "https://n23z6lq35bem5cu7gw3mhmdnya.appsync-api.us-east-2.amazonaws.com/graphql"
HEADERS = {"Content-Type": "application/json",
           "x-api-key": "da2-zzhfahbdsbhjhpalxlvu476day"
           }

createPlantStatus = """
mutation CreatePlantStatus($input: CreatePlantStatusInput!) {
    createPlantStatus(input: $input) {
        id
        moisture
        temperature
        time
        watered
    }
}
"""

def collect_plant_data():
    ##Fexch data from arduino slave device
    ## data = getData()
    return {
        "input": {
        "moisture": 123.45, #data,moisture
        "temperature": 1020, #data.temperature
        "time": get_current_time(),
        "watered": True #data.watered
    }
    }

def send_plant_data(data):
    response = requests.post(URL, json={
            'query': createPlantStatus,
            'variables': data
        }, headers=HEADERS)
    print(response.json())


def get_current_time():
    # Fetching time for the UTC timezone as an example
    response = requests.get("http://worldtimeapi.org/api/timezone/Etc/UTC")
    
    if response.status_code == 200:
        data = response.json()
        return data['datetime']
    else:
        return None

GPIO.setmode(GPIO.BCM)

## error ligth
LED_PIN = 27
GPIO.setup(LED_PIN, GPIO.OUT) 


def main():
    if time is None:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        send_plant_data(collect_plant_data())

    
if __name__ == '__main__':
    main()
    GPIO.cleanup()




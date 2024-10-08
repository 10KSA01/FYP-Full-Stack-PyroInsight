import requests
from datetime import datetime

def get_disabled_devices_panel(node):
    try:
        response = requests.get(f"http://127.0.0.1:8000/panel/{node}/disabled/")
        data = response.json()
        return str(data)
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"

def average_measurement(node, type):
    try:
        response = requests.get(f"http://127.0.0.1:8000/panel/average/{type}/{node}/")
        data = response.json()
        return str(round(data, 2))
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"

def get_latest_panel_data(node):
    try:
        response = requests.get(f'http://127.0.0.1:8000/panel/{node}/latest/')
        data = response.json()
        return data
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"

def get_average_measurement_period(node, type):
    try:
        response = requests.get(f'http://127.0.0.1:8000/panel/average/{type}/{node}/period/')
        data = response.json()
        return data
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"
    
def get_latest_device_data(id):
    try:
        response = requests.get(f'http://127.0.0.1:8000/device/{id}/latest/')
        data = response.json()
        return data
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"
    
def get_average_measurement_device(id, type):
    try:
        response = requests.get(f'http://127.0.0.1:8000/device/{id}/average/{type}/')
        if response.status_code == 500:
            return "NaN"
        data = response.json()
        return str(round(data, 2))
    except Exception as e:
        print("Error:", e)
        return "NaN"
    
def get_latest_faulty_devices_panel(node):
    try:
        response = requests.get(f'http://127.0.0.1:8000/panel/{node}/faulty/latest/')
        data = response.json()
        return data
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"
    
def get_latest_disabled_devices_panel(node):
    try:
        response = requests.get(f'http://127.0.0.1:8000/panel/{node}/disabled/latest')
        data = response.json()
        return data
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"
    
def get_latest_healthy_devices_panel(node):
    try:
        response = requests.get(f'http://127.0.0.1:8000/panel/{node}/healthy/latest/')
        data = response.json()
        return data
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"

def get_all_data_devicetype_panel(node, devicetype):
    try:
        response = requests.get(f'http://127.0.0.1:8000/panel/{node}/{devicetype}/')
        data = response.json()
        return data
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"

def get_predict_dirtiness_device(id):
    try:
        response = requests.get(f'http://127.0.0.1:8000/device/{id}/predict/dirtiness/')
        data = response.json()

        dt = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S")
        data = dt.strftime("%Y-%m-%d %H:%M")

        return data
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"
    
def get_latest_column_device_data(id, column):
    try:
        response = requests.get(f'http://127.0.0.1:8000/device/{id}/latest/{column}/')
        data = response.json()

        return data
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"
    
def get_latest_column_device_data(id, column):
    try:
        response = requests.get(f'http://127.0.0.1:8000/device/{id}/latest/{column}/')
        data = response.json()

        return data
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"
    
def get_measurement_device_period(id, type):
    try:
        response = requests.get(f'http://127.0.0.1:8000/device/{id}/{type}/period/')
        data = response.json()

        return data
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"
    
def get_measurement_device_predict(id, type):
    try:
        response = requests.get(f'http://127.0.0.1:8000/device/{id}/{type}/predict/')
        data = response.json()

        return data
    except Exception as e:
        print("Error:", e)
        return "Error fetching data"
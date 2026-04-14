import requests

def get_temperature(city):
    temps = {'boston': 45, 'paris': 52, 'london': 48}
    return temps.get(city.lower(), 'unknown')

if __name__ == '__main__':
    print(get_temperature('boston'))

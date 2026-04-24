import requests
from pprint import pprint
from dotenv import load_dotenv
import os  

load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')

url = (f'https://api.openweathermap.org/data/2.5/weather'
       f'?q=Boston&appid={API_KEY}&units=imperial')

print(url)
data = requests.get(url).json()
print(f"Worcester: {data['main']['temp']}°F")
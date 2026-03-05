import requests

url = "https://api.propella.ng/"

response = requests.get(url)
print(response.status_code)
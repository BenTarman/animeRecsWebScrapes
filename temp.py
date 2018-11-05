import requests
import re

url = 'https://myanimelist.net/animelist/Gustavo_Miranda?status=2'
page = requests.get(url)

result = re.findall(r'anime_id&quot;:\d+,&quot', page.text)


print(result[len(result) - 1])

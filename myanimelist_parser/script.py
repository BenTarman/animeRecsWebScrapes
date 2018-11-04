import xml.etree.ElementTree as ET

# want data like so
# (anime_id, name, score)
tree = ET.parse('anime.xml')
root = tree.getroot()

# print(root[1][1].text)

# store user anime in tuple format
animes = []

count = 0

# parase animes
for child in root[1:]:
    status = child.find('my_status')
    if status.text == "Completed":
        anime_id = child.find('series_animedb_id').text
        name = child.find('series_title').text
        score = child.find('my_score').text
        count += 1
        print(anime_id, name, score)

print(count)

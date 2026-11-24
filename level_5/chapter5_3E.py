import requests
import json
import csv

# Write the title and year of each movie to a CSV for every movie in this JSON file

url = "https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json"

response = requests.get(url)
movies_data = json.loads(response.text)


with open("movies_data.csv", "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Year"])
    for movie in movies_data:
        writer.writerow([movie["title"], movie["year"]])

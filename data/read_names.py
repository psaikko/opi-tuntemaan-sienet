import json

with open("webscraper/luontoportti.json", "r") as f:
    data = json.loads("".join(f.readlines()))

names = [record["name_fi"]+";"+record["name_latin"] for record in data]

with open("names", "w") as f:
    for name in names:
        f.write(name+"\n")
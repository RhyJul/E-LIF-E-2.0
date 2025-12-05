import datetime
import json
import pathlib

now = datetime.datetime.now()
filename = pathlib.Path(f"./data/{now.year}-{now.month}.json")
if not filename.exists():
    with filename.open("w") as f:
        json.dump({}, f)
        data = {}
else:
    with filename.open("r") as f:
        data = json.load(f)

print(data)


year = input("Year: ")
month = input("Month: ")


filename = pathlib.Path(f"./data/{year}-{month}.json")
if not filename.exists():
    print("No data of this month exists!")
else:
    with open(filename, "r") as infile:
        data = json.load(infile)

    print(data)
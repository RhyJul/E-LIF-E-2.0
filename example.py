import datetime
import json
import pathlib
now = datetime.datetime.now()

print(now.year, now.month, now.day)
day_report = {
    "steps": 52030,
    "sleep": 7.5,
    "sleep_quality": 1
}
data = {
    f"{now.year}-{now.month}-{now.day}": day_report
}
filename = pathlib.Path(f"./data/{now.year}-{now.month}.json")

if not filename.parent.exists():
    filename.parent.mkdir(parents=True)

with open(filename, "w") as outfile:
    json.dump(data, outfile)
import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from search.models import Plant

CSV_PATH ='plantdic_dryGarden.csv'

with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        Plant.objects.get_or_create(
            name = row['\ufeffname'],
            photo_url = row['photo_url'],
            care_difficulty = row["manageDemandNm"],
            management_level = row["manageLevelNm"],
            water_period_spring = row["waterCycleInfo"],
            sunlight = row["lighttInfo"],
            content = row["chartrInfo"]
        )



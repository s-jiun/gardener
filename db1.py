import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from search.models import Plant
CSV_PATH = 'plantdic_dryGarden.csv'

with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    data_reader = csv.DictReader(csvfile)
    static_url = '/static/dryplant_image/'
    for row in data_reader:
        Plant.objects.get_or_create(
            name=row['name'],
            growth_form=0,
            photo_url=static_url + row["name"].replace(' ', '') + '.jpeg',
            care_difficulty=row["manageDemandNm"],
            management_level=row["manageLevelNm"],
            water_period_spring=row["waterCycleInfo"],
            sunlight=row["lighttInfo"],
            content=row["chartrInfo"]
        )

import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from search.models import Plant

CSV_PATH ='plantdic_1.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    for row in data_reader:
        print(row)
    #     Plant.objects.create(



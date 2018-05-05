#!/usr/local/bin/python3.4

import os
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "papersoccer.settings")

import django
django.setup()

from schemes.models import KurnikRanking

stats_file = 'ranking_to_29_04_2018.csv'

with open(stats_file) as csvfile:
    reader = csv.DictReader(csvfile)
    players = list(reader)

for i in range(len(players)):
    add_player = KurnikRanking(player=players[i]['name'], games=players[i]['games'], ranking=players[i]['rank'])
    add_player.save()

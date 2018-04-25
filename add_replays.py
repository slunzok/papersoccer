#!/usr/local/bin/python3.4

import os
import sys
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "papersoccer.settings")

import django
django.setup()

from schemes.models import KurnikReplay

game_date = sys.argv[1]
start_id = int(sys.argv[2])
end_id   = int(sys.argv[3])+1

for id in range(start_id,end_id):

    replay = open('labs/' + game_date + '/' + str(id) + '.txt', 'r')
    replay_lines = replay.readlines()
    replay.close()

    # 1. Moves

    moves = ''

    for i in range(12,len(replay_lines)-1):
        moves += replay_lines[i].strip() + ' '

    clean_moves = re.sub(r'\d{1,2}\.', r'', moves)
    all_moves  = clean_moves.split()

    all_moves_string = ''

    i = 0

    for move in all_moves:
        if move == '1-0' or move == '0-1':
            result = move
        else:
            if i == 0:
                all_moves_string = all_moves_string + move
            else:
                all_moves_string = all_moves_string + ' ' + move
            i += 1

    # 2. Other informations

    tmp_date = replay_lines[2].strip()
    date = re.sub(r'\[Date \"(\d{4}).(\d{2}).(\d{2})\"\]', r'\3.\2.\1', tmp_date)

    tmp_time = replay_lines[7].strip()
    time = re.sub(r'\[Time \"(\d{2}):(\d{2}):(\d{2})\"\]', r'\1:\2:\3', tmp_time)

    tmp_round_time = replay_lines[8].strip()
    round_time = re.sub(r'\[TimeControl \"(\d{1,3})\"\]', r'\1', tmp_round_time)

    tmp_player1 = replay_lines[4].strip()
    player1 = re.sub(r'\[Black \"(.+?)\"\]', r'\1', tmp_player1)

    tmp_player2 = replay_lines[5].strip()
    player2 = re.sub(r'\[White \"(.+?)\"\]', r'\1', tmp_player2)

    tmp_elo1 = replay_lines[9].strip()
    elo1 = re.sub(r'\[BlackElo \"(\d{1,4})\"\]', r'\1', tmp_elo1)

    tmp_elo2 = replay_lines[10].strip()
    elo2 = re.sub(r'\[WhiteElo \"(\d{1,4})\"\]', r'\1', tmp_elo2)

    """
    print("Date: " + date + " - " + time + " - " + round_time + " sekund")
    print("Player 1: " + player1)
    print("Player 2: " + player2)
    print("ELO 1: " + elo1)
    print("ELO 2: " + elo2)
    print("Moves: " + all_moves_string)
    print("Result: " + result)
    """

    # 3. Add to database
    add_replay = KurnikReplay(name=str(id), player1=player1, player2=player2, replay_date=date, replay_time=time, replay_round=round_time, player1_elo=elo1, player2_elo=elo2, moves=all_moves_string, result=result)
    add_replay.save()


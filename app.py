import psycopg2
import generate
import csv
import pandas as pd
from helpers import reset_database

with psycopg2.connect(dbname="library", user="python", password="python", host="127.0.0.1", port="5432") as conn:
    with conn.cursor() as cur:

        # A chaque fois qu'on lance le script, on reset la base pour avoir les mêmes résultats
        reset_database(cur)
        generate.ajout_utilisateurs(cur)
        generate.ajout_games(cur)
        generate.liaison_tables(cur)
        generate.ajout_genres(cur)
        generate.ajout_genres(cur)
        generate.statsCSV(cur)
        generate.worstGamesByYears(cur)
        generate.NbGamesUsersMoy(cur)
        generate.NbGamesByGenre(cur)


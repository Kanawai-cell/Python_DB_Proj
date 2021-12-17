from faker import Faker
import json
import datetime

faker = Faker()

def user_first_name():
    return faker.first_name()

def user_last_name():
    return faker.last_name()
    
def user():
    return (user_first_name(), user_last_name())

def game():
    return (game_name(), faker.past_datetime())

def game_name():
    return ''.join(faker.words())

def game_addedBy():
    return faker.random_int()

def game_metacritic():
    return faker.random_int(min=0, max=100)

def game_title_meta():
    return (game_name(), game_metacritic())

def game_name_addedby():
    return (game_name(), game_addedBy())

def ajout_utilisateurs(cur):
    # On ajoute 10 utilsateurs
    for i in range(200):
        cur.execute('insert into "users" (first_name, last_name) values (%s, %s);', generate.user())

def ajout_games(cur):
    # On la joue safe et on recompte le nombre d'utilisateurs depuis la base pour plus tard
    cur.execute('select count(*) from "users";')
    # Ici on a un [0] car fetchone() renvoi toujours un tuple, même avec une seule valeur
    user_count = cur.fetchone()[0]

    cur.execute('select users_id from "users";')
    users = cur.fetchall()
    #print(users)

    # Loop through the resulting list and print each user name, along with a line break:
    # for i in range(len(users)):
    #     print(''.join( str(users[i]) ) )
    #tuple to string
    #str = ''.join(tuple1)

    # On ajoute 100 jeux
    for i in range(100):
        cur.execute('insert into "game" (title, release) values (%s, %s);', generate.game())

def liaison_tables(cur):
    cur.execute('select users_id from "users";')
    users = cur.fetchall()
    # On ajoute 100 liaison entre les jeux et les utilisateurs 
    liaison = 'insert into "game" (title, users_id) values ( %s , %s )'
    insert = ( generate.game_name(), users[i])
    for i in range(100):
        cur.execute(liaison, insert)

def ajout_genres(cur):
    # On ajoute 100 genres 
    strings = str(generate.game_name())
    inserts = 'insert into "genre" ( name ) values ( %s )'

    for i in range(200):
        #print(type(inserts), type(strings))
        cur.execute(inserts, (strings, ) )

def ajout_genres(cur):
    # On ajoute 100 liaison avec jeux
    str_liaison ='insert into "game_genres" ( game_id, genre_id ) values ( %s , %s )'
    insert_liaison = (users[i], users[100-i])
    for i in range(100):
        cur.execute(str_liaison, insert_liaison)

def statsCSV(cur):
    # [ CSV ]            
    with open('./exports/stats.csv', 'w') as file:
        # [ . . . ]
        cur.execute(
            # [ La requête ]
            '''select
                g.title,
                g.metacritic,
                date_part('year', g."release") as release_year
            from game g
            where
                g.metacritic = (
                    select max(metacritic)
                    from game
                    where date_part('year', "release") = date_part('year', g."release")
                )
            order by release_year'''
        )

        data = cur.fetchall()
        print(data)
        # > [("Game1", 99, 2000), ("Game2", 95, 2001), ("Game3", 87, 2002)]
    # for i in range(len(data)):
    #     for j in range(len(data[i])):
    #         ligne = ''.join( str(data[i][i]) + ';' )
    #         file.write(ligne)
        df = pd.DataFrame(data, columns=['title', 'metacritic', 'release'])
        df.to_csv('./exports/stats.csv', sep=';')

def worstGamesByYears(cur):
# [ La liste des pire jeux par années ]  
    # [ CSV ]            
    with open('./exports/worstGamesByYears.csv', 'w') as file:
        # [ . . . ]
        cur.execute(
            # [ La requête ]
            '''select
                g.title,
                g.metacritic,
                date_part('year', g."release") as release_year
            from game g
            where
                g.metacritic = (
                    select max(metacritic)
                    from game
                    where date_part('year', "release") = date_part('year', g."release")
                )
            order by release_year ASC,
            metacritic DESC'''
        )

        data = cur.fetchall()
        print(data)
        df = pd.DataFrame(data, columns=['title', 'metacritic', 'release'])
        df.to_csv('./exports/worstGamesByYears.csv', sep=';')

def NbGamesUsersMoy(cur):
# [ Le nombre de jeux ajoutés par utilisateur, ainsi que la moyenne de leurs scores ]  
    # [ CSV ]            
    with open('./exports/NbGamesUsersMoy.csv', 'w') as file:
        # [ . . . ]
        cur.execute(
            # [ La requête ]
            '''select
                sum(g.users_id),
                u.users_id,
                AVG(g.metacritic)
            from game g, users u
            group by 
                u.users_id,
                g.users_id,
                g.metacritic
            '''
        )

        data = cur.fetchall()
        print(data)
        df = pd.DataFrame(data, columns=['user', 'Nb_Games', 'average_Score'])
        df.to_csv('./exports/NbGamesUsersMoy.csv', sep=';')

def NbGamesByGenre(cur):
# [ Le nombre de jeux par genre ]  
    # [ CSV ]            
    with open('./exports/NbGamesByGenre.csv', 'w') as file:
        # [ . . . ]
        cur.execute(
            # [ La requête ]
            '''select
                COUNT(ga.title) AS Title,
                ge.genre_id
            from game ga, game_genres g_g, genre ge
            where
                ga.game_id = g_g.game_id AND 
                g_g.genre_id = ge.genre_id
            group by
            Title,
            ge.genre_id
            '''
        )

        data = cur.fetchall()
        print(data)
        df = pd.DataFrame(data, columns=['Nb_Games', 'Genre'])
        df.to_csv('./exports/NbGamesByGenre.csv', sep=';')

def parse_game(gametuple):
    (id, title, added_at, metacritic, pegi, release, added_by) = gametuple
    return {
        '_id': id,
        'title': title,
        'added_at': added_at,
        'added_by': added_by,
        'infos': {
            'metacritic': metacritic,
            'pegi': pegi,
            'release': release,
            'genres': []
        }
    }

class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return (str(z))
        else:
            return super().default(z)

def game_table(cur):
    cur.execute('select * from "game"')
    res = cur.fetchall()

    games = list(map(parse_game, res))
    with open(f'./migrations/games.json', 'w') as file:
        file.write(json.dumps(games, cls=DateTimeEncoder))
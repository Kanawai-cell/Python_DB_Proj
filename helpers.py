import psycopg2

def reset_database(cur) : 

        cur.execute('''DROP TABLE IF EXISTS "game_genres";''')
        cur.execute('''DROP TABLE IF EXISTS "game";''')
        cur.execute('''DROP TABLE IF EXISTS "users";''')
        cur.execute('''DROP TABLE IF EXISTS "genre";''')

        cur.execute('''create table "users" (
            users_id serial primary key,
            first_name text not null,
            last_name text,
            created_at timestamp default current_timestamp
        );''')
        cur.execute('''create table "game" (
            game_id serial primary key,
            title text not null,
            metacritic int,
            users_id int,
            pegi text,
            release timestamp default current_timestamp,
            CONSTRAINT added_by
                FOREIGN KEY (users_id)
                    REFERENCES users(users_id) ON DELETE CASCADE
        );''')
        cur.execute('''create table "genre" (
            genre_id serial primary key,
            name text not null
        );''')
        cur.execute('''create table "game_genres" (
            game_id int,
            genre_id int,
            CONSTRAINT fk_game_id
                FOREIGN KEY (game_id)
                    REFERENCES game(game_id) ON DELETE CASCADE,
            CONSTRAINT fk_genre_id
                FOREIGN KEY (genre_id) 
                    REFERENCES genre(genre_id) ON DELETE CASCADE
        );''')
        cur.execute('grant all privileges on all tables in schema public to python;')
        cur.execute('grant all privileges on all sequences in schema public to python;')


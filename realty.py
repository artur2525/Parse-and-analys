import sqlite3
import psycopg2
from datetime import datetime as dt

def check_database(offer):
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"
    with psycopg2.connect(conn_string)  as connection:
        cursor = connection.cursor()
        for data in offer:
            avito_id = data[0]
            cursor.execute(
                """
                SELECT offers.avito_id FROM offers WHERE offers.avito_id = %s
            """,
                [avito_id]
            )
            result = cursor.fetchone()
            if result is None:
                cursor.execute(
                    """
                    INSERT INTO offers (avito_id, price,advert, year, race, address, url, created_at) 
                    VALUES (%s, %s, %s, %s, %s,  %s, %s, %s)
                """,
                (int(data[0]), float(data[1]),data[2], data[3], data[4], data[5], data[6], dt.now())
                )
                connection.commit()
                print(f"Объявление {data[0]} добавлено в базу данных")


#phone_number TEXT NOT NULL,
#text TEXT,
#online_display TEXT NOT NULL,

def create_table():
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"
    connection = psycopg2.connect(conn_string) 
    cursor = connection.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS offers (
                    id SERIAL PRIMARY KEY,
                    avito_id bigint NOT NULL,
                    price REAL NOT NULL,
                    advert TEXT NOT NULL,
                    year INT NOT NULL,
                    race BIGINT NOT NULL,
                    address TEXT NOT NULL,
                    url TEXT NOT NULL,
                    created_at Timestamp  WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
    """
    )
    connection.commit()
    connection.close()
'''result = (
                    avito_id,
                    price,
                    advert,
                    year, 
                    race,
                    address,
                    url,
                )'''

            
def main():
    create_table()


if __name__ == "__main__":
    main()

import pandas as pd
import sqlite3
import psycopg2

def exporting():
    conn_string = "host='localhost' dbname='postgres' user='postgres' password='password'"
    conn = psycopg2.connect(conn_string) 
    cur = conn.cursor()
    q="SELECT * from offers"
    cur.execute(q)
    df = pd.DataFrame(cur.fetchall())
    print(df.columns)
    df[8] = df[8].apply(lambda a: pd.to_datetime(a).date()) 
    df.to_excel(r"result.xlsx")


if __name__ == "__main__":
    exporting()

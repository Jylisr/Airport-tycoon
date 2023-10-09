"""Airport Tycoon

By: Juho, Amaan, German, Chedel, Nhi

Dependencies: mysql.connector
"""

import mysql.connector
from mysql.connector.types import RowType
from typing import List

from database import modify_database


# copy paste function below to the database file


def fetch_players(cursor) -> List[RowType]:
    cursor.execute("select * from goal;")
    highscore_list = cursor.fetchall()
    return highscore_list


def start_game() -> str:
    print("Welcome to Airport Tycoon!")
    print("You have now entered the wonderful world of airportopia.")
    print("I see the spirit of a future tycoon in you.")
    print("What is your name?")
    name = str(input(""))
    return name


def name_to_table(cursor, name):
    query = f"insert into game(screen_name) values ('{name}');"
    cursor.execute(query)
    # goal table changes need to be kept in mind


def name_check(name, highscore_list) -> bool:
    for i in highscore_list:
        if i[1] == name:
            print("Looks like you've already attempted the tycoon life")
            return False
    return True


def high_score(highscore_list):
    print(
        "So as you're new around here let me show you the people that have left their mark here already"
    )
    print("Name, Score, Time")
    for i in range(5):
        print(highscore_list[i])


def main():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            database="flight_game",
            user="user",
            password="password",
            autocommit="True",
        )
        cursor = connection.cursor()
        modify_database(cursor)
        player_name = start_game()  # game starts
        player_table = fetch_players(cursor)  # players list is retrieved
        if name_check(player_name, player_table):
            print("Ah, So you are a rookie.")
            print("Welcome again to this world")
            name_to_table(
                cursor, player_name
            )  # name checked and name is added to database
        high_score(player_name)  # high score is printed

        while True:  # Game loop
            break

        # Close the connection
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        # Handle the error (database not live or doesn't exist)


if __name__ == "__main__":
    main()

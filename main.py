"""Airport Tycoon

By: Juho, Amaan, German, Chedel, Nhi

Dependencies: mysql.connector
"""

import datetime
from sys import exception
import mysql.connector
from mysql.connector.types import RowType
from typing import Any, List

import database


def get_name() -> str:
    name = str(input("What is your name?: "))
    return name


def name_to_table(cursor, name):
    query = f"insert into game(screen_name) values ('{name}');"
    cursor.execute(query)
    # goal table changes need to be kept in mind


def name_check(name, some_list) -> bool:
    for i in some_list:
        if i[4] == name:
            return False
    return True


# if you dont understand what is going on here, RTFM "classes"
class GameState:
    def __init__(self):
        # connects to database
        self.try_to_connect()
        database.modify_database(self.cursor)
        # players list is retrieved
        self.player_table = database.fetch_players(self.cursor)
        # check player name not reserved, and use the name
        self.get_name()
        # game variables
        self.player_score: int = 0
        self.game_time_limit = datetime.time(minute=5)
        self.player_owned_properties: list[str] = []

    def try_to_connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="127.0.0.1",
                port=3306,
                database="flight_game",
                user="user",
                password="password",
                autocommit=True,
            )
            # NOTE: cursor variable is set here too
            self.cursor = self.connection.cursor()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            # Handle the error (database not live or doesn't exist)

    def deinit(self):
        self.connection.close()

    def advance_time(self, how_much):
        pass

    def ask_for_decision(self):
        # buy?
        # fly?
        # auction?
        #
        pass

    def print_high_score(self):
        print("Let me show you the people that have left their mark here already")
        print("Name, Score, Time")
        for i in range(5):
            print(f"{self.player_table[i][4]}, Score here, Time here")

    def get_name(self):
        while True:
            name = get_name()
            if name_check(name, self.player_table):
                print("Ah, So you are a rookie.")
                print("Welcome again to this world")
                name_to_table(
                    self.cursor, name
                )  # name checked and name is added to database
                self.player_name = name
                break
            else:
                print("Looks like you've already attempted the tycoon life")
                print("(Player with that name already played, choose a new name.)")


def main():
    print("Welcome to Airport Tycoon!")
    print("You have now entered the wonderful world of airportopia.")
    print("I see the spirit of a future tycoon in you.")

    # # # Intro loop
    game_state = GameState()

    # # # Game loop
    while True:
        break
        # show time cost
        # show location


if __name__ == "__main__":
    main()

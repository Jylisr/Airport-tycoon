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


def get_name_input() -> str:
    name = str(input("What is your name?: "))
    return name


def name_to_table(cursor, name):
    co2_budget = 10000
    query = f"insert into game(screen_name, co2_budget,co2_consumed) values ('{name}',{co2_budget},0);"
    cursor.execute(query)
    # goal table changes need to be kept in mind


def name_check(name, some_list) -> bool:
    for i in some_list:
        if i[4] == name:
            return False
    return True
def calculate_distance_between_airports(icao1, icao2):
    from geopy.distance import geodesic
    coords1 = get_airport_coordinates(icao1)
    coords2 = get_airport_coordinates(icao2)
    if coords1 and coords2:
        # Create geodesic objects using the coordinates
        airport1_coords = (coords1[0], coords1[1])
        airport2_coords = (coords2[0], coords2[1])
        distance = geodesic(airport1_coords, airport2_coords).kilometers
        return distance
    else:
        return None
def fly_to(location):
    CO2_KG_USED_PER_KM_FLOWN = 0.133
    while co2_budget > 0:
        print("Current CO2 Budget: {} KG".format(co2_budget))
        icao1 = input("Enter ICAO code of your current airport: ")
        icao2 = input("Enter ICAO code of your destination airport: ")

        distance = calculate_distance_between_airports(icao1, icao2)

        if distance is not None:
            co2_consumed = distance * CO2_KG_USED_PER_KM_FLOWN
            if co2_consumed <= co2_budget:
                co2_budget -= co2_consumed
                print(f"Successfully flew from {icao1} to {icao2}.")
                print(f"Distance: {distance:.2f} kilometers")
                print(f"CO2 Consumed: {co2_consumed:.2f} kilograms")
                print(f"Remaining CO2 Budget: {co2_budget:.2f} kilograms")
            else:
                print("You don't have enough CO2 budget for this flight.")
                break
        else:
            print("Distance calculation failed. Please check the ICAO codes and ensure they exist in the database.")


def ask_for_decision():
    # buy?
    # fly?
    # auction?
    choice = str(
        input(
            """
What do you want to do now?
(F)ly
"""
        )
    )
    match choice:
        case "f" | "F":
            fly_to("location")



def print_high_score(self):
    print("Let me show you the people that have left their mark here already")
    print("Name, Score, Time")
    for i in range(5):
        print(f"{self.player_table[i][4]}, Score here, Time here")


def get_name(cursor, player_table):
    while True:
        name = get_name_input()
        if name_check(name, player_table):
            print("Ah, So you are a rookie.")
            print("Welcome again to this world")
            name_to_table(cursor, name)  # name checked and name is added to database
            return name
        else:
            print("Looks like you've already attempted the tycoon life")
            print("(Player with that name has already played, choose a new name.)")


def place_player_in_random_airport(cursor):
    return database.get_random_airport(cursor)


def main():
    print("Welcome to Airport Tycoon!")
    print("You have now entered the wonderful world of airportopia.")
    print("I see the spirit of a future tycoon in you.")

    # # # Intro loop
    # game = GameState()

    # connects to database
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        database="flight_game",
        user="user",
        password="password",
        autocommit=True,
    )
    cursor = connection.cursor()
    database.modify_database(cursor)
    # players list is retrieved
    player_table = database.fetch_players(cursor)
    # check player name not reserved, and use the name
    player_name = get_name(cursor, player_table)
    # game variables

    player_score = 0
    game_time_limit = datetime.time(minute=5)
    player_owned_properties: list[str] = []
    co2_budget = 10_000
    current_airport = ""

    # # # Game loop

    # spawn in random airport; have co2_budget; have money
    # goto to airports nearby; costs co2
    # buy shops in airports; or end early; costs money
    # "simulate" a year of operation => calculate score + add unspent money

    # shop data:
    #   price
    #   revenue generation
    #   name

    while True:
        break
        # show time cost
        # show location

    # Close database conn
    connection.close()


if __name__ == "__main__":
    main()

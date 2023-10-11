"""Airport Tycoon

By: Juho, Amaan, German, Chedel, Nhi

Dependencies: mysql.connector
"""

import datetime
from sys import exception
import mysql.connector
from mysql.connector import cursor
from mysql.connector.types import RowType
from typing import Any, List

import database

import random

# connects to database
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    database="flight_game",
    user="user",
    password="password",
    autocommit=True,
)


def get_name_input() -> str:
    name = str(input("What is your name?: "))
    return name

def name_to_table(cursor, name):
    co2_budget = 10000
    query = f"insert into game(screen_name, co2_budget,co2_consumed) values ('{name}',{co2_budget},0);"
    cursor.execute(query)
    # goal table changes need to be kept in mind


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

cursor = connection.cursor()
database.modify_database(cursor)
# players list is retrieved
player_table = database.fetch_players(cursor)
# check player name not reserved, and use the name
player_name = get_name(cursor, player_table)
# game variables

airports = database.fetch_airport(cursor)
player_score = 0
game_time_limit = datetime.time(minute=5)
player_owned_properties = []
co2_budget = 10_000
current_airport = ""
player_money = 10_000





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



def buy():
    def generate_random_shop(shop_names):
        name = random.choice(shop_names)
        price = random.randint(1000, 10000)
        revenue_per_month = random.randint(1000, 5000)
        return name, price, revenue_per_month

    #Loop
    import random

    def buy():
        def generate_random_shop(shop_names):
            name = random.choice(shop_names)
            price = random.randint(1000, 10000)
            revenue_per_month = random.randint(1000, 5000)
            return name, price, revenue_per_month

        # Loop
        while True:
            shop_names = ["Duty-Free Shop", "Coffee House", "Electronics Store", "Bookstore", "Gift Shop",
                          "Fashion Boutique"]
            num_shops = random.randint(1, 5)
            print("Buy Shops:")
            for _ in range(num_shops):
                shop_name, acquisition_price, revenue_per_month = generate_random_shop(shop_names)
                print(f"Shop Name: {shop_name}")
                print(f"Acquisition Price: {acquisition_price}")
                print(f"Revenue per month: {revenue_per_month}")

                # Appends the player money and owned property names in player_owned_properties list upon yes decision.
                if player_money >= acquisition_price:
                    buy_decision = input("Do you want to buy this shop? (Yes/No):")
                    if buy_decision.lower() == "yes":
                        player_money -= acquisition_price
                        player_owned_properties.append({
                            "name": shop_name,
                            "revenue": revenue_per_month
                        })
                        print(f"Congratulations! You bought {shop_name} for ${acquisition_price}.")
                    else:
                        print(f"You chose not to buy {shop_name}")
                else:
                    print("You don't have enough money to buy this shop.")


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

def place_player_in_random_airport(cursor):
    return database.get_random_airport(cursor)

def exitgame():
    if co2_budget <= 0:
        return True
    else:
        return False

def calculate_final_score(player_money, property_revenues):
    total_revenue = 0
    for property in property_revenues:
        total_revenue += property ['revenue'] * 12
    final_score = total_revenue + player_money
    return final_score

def main():
    print("Welcome to Airport Tycoon!")
    print("You have now entered the wonderful world of airportopia.")
    print("I see the spirit of a future tycoon in you.")
    while True:

    # # # Intro loop
    # game = GameState()



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

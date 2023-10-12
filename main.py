"""Airport Tycoon

By: Juho, Amaan, German, Chedel, Nhi

Dependencies: mysql.connector
"""

import datetime
import geopy
from sys import builtin_module_names, exception
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


def name_to_table(cursor, name, co2_budget):
    query = f"insert into game(screen_name, co2_budget,co2_consumed) values ('{name}',{co2_budget},0);"
    cursor.execute(query)
    # goal table changes need to be kept in mind


def name_check(name, some_list) -> bool:
    for i in some_list:
        if i[4] == name:
            return False
    return True


def get_name(cursor, player_table, co2_budget):
    while True:
        name = get_name_input()
        if name_check(name, player_table):
            print("Ah, So you are a rookie.")
            print("Welcome to this world")
            name_to_table(
                cursor, name, co2_budget
            )  # name checked and name is added to database
            return name
        else:
            print("Looks like you've already attempted the tycoon life")
            print("(Player with that name has already played, choose a new name.)")


def get_airport_coordinates(icao):
    sql = "SELECT latitude_deg, longitude_deg FROM airport WHERE ident = %s"
    cursor = connection.cursor()
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        print(f"Airport with ICAO code {icao} not found in the database.")
        return None


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


def fly_to(airports, current_airport, location, co2_budget, co2_consumed):
    CO2_KG_USED_PER_KM_FLOWN = 0.133
    print("Current CO2 Budget: {} KG".format(co2_budget))
    table_of_airport_names_for_id_extraction = []
    for airport in airports:
        table_of_airport_names_for_id_extraction.append(airport[0])
    idx_of_current_airport = table_of_airport_names_for_id_extraction.index(
        current_airport
    )

    icao1 = airports[idx_of_current_airport][3]
    icao2 = airports[location][3]

    distance = calculate_distance_between_airports(icao1, icao2)

    if distance is not None:
        co2_consumed += distance * CO2_KG_USED_PER_KM_FLOWN
        if co2_consumed <= co2_budget:
            co2_budget -= co2_consumed
            print(
                f"Successfully flew from {current_airport[0]} to {airports[location][0]}."
            )
            print(f"Distance: {distance:.2f} kilometers")
            print(f"CO2 Consumed: {co2_consumed:.2f} kilograms")
            print(f"Remaining CO2 Budget: {co2_budget:.2f} kilograms")
            return (airports[location][0], co2_budget, co2_consumed)
        else:
            print("You don't have enough CO2 budget for this flight.")
    else:
        print(
            "Distance calculation failed. Please check that you have not visited airport already."
        )


def generate_random_shop():
    num_shops = random.randint(1, 7)
    shop_names = [
        "Duty-Free Shop",
        "Coffee House",
        "Electronics Store",
        "Bookstore",
        "Gift Shop",
        "Fashion Boutique",
        "Restaurant",
    ]
    name = random.choice(shop_names)
    print("Buy Shops:")
    list_of_shops = []
    for _ in range(num_shops):
        name = random.choice(shop_names)
        price = random.randint(1000, 8000)
        revenue_per_month = random.randint(1000, 5000)
        list_of_shops.append([name, price, revenue_per_month])
    return list_of_shops


def buy(list_of_shops, player_money, choice):
    # Appends the player money and owned property names in player_owned_properties list upon yes decision.
    if player_money >= list_of_shops[choice][1]:
        buy_decision = input("Do you want to buy this shop? (Yes/No):")
        if buy_decision.lower() == "yes":
            player_money -= list_of_shops[choice][1]
            print(
                f"Congratulations! You bought {list_of_shops[choice][0]} for ${list_of_shops[choice][1]}."
            )
            return (list_of_shops, player_money)
        else:
            print(f"You chose not to buy {list_of_shops[choice][0]}")
    else:
        print("You don't have enough money to buy this shop.")


def print_high_score(player_table):
    print("Let me show you the people that have left their mark here already")
    print("Name, Score, Time")
    for i in range(5):
        try:
            print(
                player_table[i][4],
                player_table[i][2],
                player_table[i][3],
                sep="|",
            )
        except Exception:
            continue


def place_player_in_random_airport(cursor, airports, player_name):
    PlInRanAir = database.get_random_airport(cursor, airports)
    print(f"{player_name}, you are in {PlInRanAir[0]}")
    return PlInRanAir


def print_random_airports(airports):
    for i in range(10):
        j = random.randrange(0, len(airports))
        print(j, ". ", airports[j][0], sep="|")


def exitgame(co2_budget):
    if co2_budget <= 0:
        return True
    else:
        return False


def calculate_final_score(player_money, property_revenues):
    total_revenue = 0
    for property in property_revenues:
        total_revenue += property["revenue"] * 12
    final_score = total_revenue + player_money
    return final_score


def main():
    cursor = connection.cursor()
    database.modify_database(cursor)
    # players list is retrieved
    player_table = database.fetch_players(cursor)

    # game variables

    airports = database.fetch_airport(cursor)
    player_score = 0
    game_time_limit = datetime.time(minute=5)
    player_owned_properties = []
    co2_budget = 10_000
    co2_consumed = 0
    current_airport = ""
    player_money = 10_000
    print("Welcome to Airport Tycoon!")
    print("You have now entered the wonderful world of airportopia.")
    print("I see the spirit of a future tycoon in you.")
    player_name = get_name(cursor, player_table, co2_budget)
    print_high_score(player_table)
    PlInAir = place_player_in_random_airport(cursor, airports, player_name)
    current_airport = PlInAir[0]
    # check player name not reserved, and use the name

    while True:
        print(f"{player_name}, you are in {current_airport}")
        print(f"You have ${player_money} left, and {co2_budget} co2 left")
        list_of_shops = generate_random_shop()
        print(list_of_shops)
        choice = str(
            input(
                """
        What would you like to do now?
        (F)ly to a different airport
        (B)uy a shop at this airport
        (E)xit game
            """
            )
        )
        match choice:
            case "f" | "F":
                print_random_airports(airports)
                location = int(
                    input(
                        "Enter the serial number of the airport you would like to go to? "
                    )
                )
                result = fly_to(
                    airports, current_airport, location, co2_budget, co2_consumed
                )
                current_airport = result[0]
                co2_budget = result[1]
                co2_consumed = result[2]

            case "b" | "B":
                shop_choice = int(input("Which shop would you like to buy? "))
                result = buy(list_of_shops, player_money, shop_choice)
                player_owned_properties.append(result[0])
                player_money = result[1]
                print(f"Congratulations! You have purchased ")
            case "e" | "E":
                break

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

'''Airport Tycoon

By: Juho, Amaan, German, Chedel, Nhi

Dependencies: mysql.connector
'''

import mysql.connector

connection = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='',
    user='',
    password='',
    autocommit='True'
)
cursor=connection.cursor()


# copy paste function below to the database file

def fetch_players():
    cursor.execute("select * from goal;")
    highscore_list=cursor.fetchall()
    return highscore_list

def start_game():
    print("Welcome to Airport Tycoon!")
    print("You have now entered the wonderful world of airportopia.")
    print("I see the spirit of a future tycoon in you.")
    print("What is your name?")
    name=int(input(""))
    return name
def name_to_table(name):
    query = f"insert into goal(screen_name) values ('{name}');"
    cursor.execute(query)
    #goal table changes need to be kept in mind
def name_check(name,highscore_list):
    for i in highscore_list:
        if i[0]==name:
            print("Looks like you've already attempted the tycoon life")
            break
        else:
            print("Ah, So you are a rookie.")
            print("Welcome again to this world")
            name_to_table(name)

def high_score(highscore_list):
    print("So as you're new around here let me show you the people that have left their mark here already")
    print("Name, Score, Time")
    for i in range(5):
        print(highscore_list[i])

#main
player_name = start_game() #game starts
player_table = fetch_players() #players list is retrieved
name_check(player_name, player_table) # name checked and name is added to database
high_score(player_name) #high score is printed
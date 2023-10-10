import mysql.connector
from mysql.connector.types import RowType
from typing import List


def modify_database(cursor):
    # checks if game.player field auto-increments and sets it
    query_drop_goal_reached = """
if exists(
    select schema_name from information_schema.schemata where schema_name = 'goal_reached'
)
then
    -- Drop the foreign key constraints first
    ALTER TABLE goal_reached DROP FOREIGN KEY goal_reached_ibfk_1;
    ALTER TABLE goal_reached DROP FOREIGN KEY goal_reached_ibfk_2;

    -- Drop the table
    DROP TABLE IF EXISTS goal_reached
;
end if
;
    """
    query_make_player_id_auto_inc = """
if not exists (
    select column_name, column_key
    from information_schema.columns
    where
        table_schema = 'flight_game'
        and table_name = 'game'
        and column_name = 'id'
        and column_key = 'PRI'
        and extra = 'auto_increment'
)
then
    alter table game modify id int auto_increment
;
end if
;
    """
    cursor.execute(query_drop_goal_reached, multi=True)
    cursor.execute(query_make_player_id_auto_inc)


def fetch_players(cursor) -> List[RowType]:
    cursor.execute("select * from game;")
    highscore_list = cursor.fetchall()
    # NOTE: debug print whole table
    # print("DEBUG: game table start")
    # print(highscore_list)
    # print("DEBUG: game table end")
    return highscore_list


def write_score(cursor):  # TODO
    pass


def get_random_airport(cursor):
    query = """

    """

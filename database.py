def modify_database(cursor):
    # checks if game.player field auto-increments and sets it
    query_drop_goal_reached = """
-- Drop the foreign key constraints first
ALTER TABLE goal_reached DROP FOREIGN KEY goal_reached_ibfk_1;
ALTER TABLE goal_reached DROP FOREIGN KEY goal_reached_ibfk_2;

-- Drop the table
DROP TABLE IF EXISTS goal_reached;
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

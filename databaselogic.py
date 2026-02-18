import sqlite3

DB_PATH = "staging.db"


def create_datatable() -> None:
    with sqlite3.connect(DB_PATH) as conn:

        conn.execute(
            """CREATE TABLE IF NOT EXISTS sections (
                section_name TEXT PRIMARY KEY,
                tables int null
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS tables (
                table_id INTEGER PRIMARY KEY,
                coordinates TEXT,
                item_type TEXT
            )"""
        )

def insert_section_data(table_id:int, table_coordinates:int, section_name:str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO sections (section_name,table_id, table_coordinates) VALUES (?, ?, ?)",
            (int(table_id), int(table_coordinates), section_name),
        )
def delete_database(table:str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        try:
            conn.execute(f"DROP TABLE {table}")
            (str(table))
            print ("Table deleted successfully")
        except sqlite3.Error as e:
            print(f"Error deleting table: {e}")
def delete_sections(section_name:str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(f"DELETE FROM sections WHERE section_name = '{section_name}'")
        (str(section_name))
def insert_table_data(table_id:int, table_coordinates:int, section_name:str, item_type=None) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO tables (table_id,coordinates,item_type) VALUES (?,?)",
            (int(table_id), int(table_coordinates),int(item_type)),
        )
import sqlite3

DB_PATH = "staging.db"


def create_datatable() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS servers (
                name TEXT PRIMARY KEY,
                section TEXT,
                rotation INTEGER,
                amount_of_tables INTEGER 
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS sections (
                table_id INTEGER,
                table_coordinates TEXT,
                section_name TEXT
            )"""
        )


def insert_server_data(server_name: str, section: str, rotation: int, amount_of_tables: int) -> None:
    name = server_name.strip()
    section = section.strip()
    if not name:
        raise ValueError("Server name cannot be empty")

    with sqlite3.connect(DB_PATH) as conn:
        with conn:
            conn.execute(
            "INSERT INTO servers (server_name, section, rotation, amount_of_tables) VALUES (?, ?, ?, ?)",
            (server_name, section, int(rotation), int(amount_of_tables)),
        )
def insert_section_data(table_id:int, table_coordinates:int, section_name:str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        with conn:
            conn.execute(
            "INSERT INTO sections (table_id, table_coordinates, section_name) VALUES (?, ?, ?)",
            (int(table_id), int(table_coordinates), section_name),
        )
def rename_column(table_name:str, old_column_name:str, new_column_name:str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        with conn:
            conn.execute(f"ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name}")


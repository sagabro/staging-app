import sqlite3

DB_PATH = "staging.db"


def create_datatable() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS servers (
                name TEXT,
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


def insert_server_data(name: str, section: str, rotation: int, amount_of_tables: int) -> None:
    name = name.strip()
    section = section.strip()
    if not name:
        raise ValueError("Server name cannot be empty")
    if not section:
        raise ValueError("Section cannot be empty")

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO servers (name, section, rotation, amount_of_tables) VALUES (?, ?, ?, ?)",
            (name, section, int(rotation), int(amount_of_tables)),
        )
def insert_section_data(table_id:int, table_coordinates:int, section_name:str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO sections (table_id, table_coordinates, section_name) VALUES (?, ?, ?)",
            (int(table_id), int(table_coordinates), section_name),
        )
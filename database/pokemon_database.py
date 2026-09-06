import sqlite3
import json
from pathlib import Path


DATABASE_PATH = Path(__file__).parent.parent / "data" / "pokemon.db"


def get_connection():
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            data TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moves (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            data TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

def save_pokemon(pokemon):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO pokemon (name, data)
        VALUES (?, ?)
        """,
        (
            pokemon["name"],
            json.dumps(pokemon)
        )
    )

    connection.commit()
    connection.close()


def get_pokemon(name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT data
        FROM pokemon
        WHERE name = ?
        """,
        (name.lower(),)
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return None

    return json.loads(result[0])

def save_move(move):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO moves (name, data)
        VALUES (?, ?)
        """,
        (
            move["name"],
            json.dumps(move)
        )
    )

    connection.commit()
    connection.close()


def get_move(name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT data
        FROM moves
        WHERE name = ?
        """,
        (name.lower(),)
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return None

    return json.loads(result[0])


if __name__ == "__main__":

    initialize_database()

    test_pokemon = {
        "name": "rillaboom",
        "types": ["grass"],
        "stats": {
            "hp": 100,
            "attack": 125
        },
        "abilities": [
            "overgrow",
            "grassy-surge"
        ]
    }

    save_pokemon(test_pokemon)

    result = get_pokemon("rillaboom")

    print(result)
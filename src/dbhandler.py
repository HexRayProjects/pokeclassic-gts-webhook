import sys, sqlite3

from typing import List, Tuple, Union, Optional
from .gtsentry import GTSEntry


def commit_entry(cur: sqlite3.Cursor, entry_hash: str) -> None:
    cur.execute("INSERT INTO entries VALUES (?)", (entry_hash,))


def delete_entry(cur: sqlite3.Cursor, entry_hash: str) -> None:
    cur.execute("DELETE FROM entries WHERE dhash=?", (entry_hash,))


def safe_table_create(cur: sqlite3.Cursor) -> None:
    cur.execute("CREATE TABLE IF NOT EXISTS entries(dhash TEXT)")


def print_db(cur: sqlite3.Cursor) -> None:
    cur.execute("SELECT * FROM entries")
    for entry in cur.fetchall():
        print(entry)


def drop_all_entries(cur: sqlite3.Cursor) -> None:
    cur.execute("DELETE FROM entries")


def get_db_entries(cur: sqlite3.Cursor) -> List[str]:
    cur.execute("SELECT * FROM entries")
    return [_[0] for _ in cur.fetchall()]


if __name__ == "__main__":
    dummy_entry = GTSEntry(
        nickname = "Joshawott",
        species = "Oshawott",
        species_icon = "https://pkmnclassic.net/images/pkmn-lg/501.png",
        dex_no = "501",
        nature = "Jolly",
        held_item = "Master Ball",
        ability = "Torrent",
        level = "69",
        gender = "♂",
        ball_name = "Poké Ball",
        ball_icon = "https://pkmnclassic.net/images/item-sm/3004.png",
        has_pkrs = True,
        offered_by = "Ass Ktchup",
        wanted_species = "Arceus",
        wanted_species_icon = "https://pkmnclassic.net/images/pkmn-sm/493-normal.png",
        wanted_dex_no = "483",
        wanted_level = 1,
        wanted_gender = "",
        upload_date = "Thursday, October 14, 2021 10:37 PM",
    )

    con = sqlite3.connect("test.db")
    cur = con.cursor()

    safe_table_create(cur)
    _hash = str(hash(dummy_entry))
    commit_entry(cur, _hash)

    print_db(cur)

    con.commit()
    con.close()

import sys, sqlite3

from typing import List, Tuple, Union, Optional
from .gtsentry import GTSEntry


class DBHandler:
    def __init__(self, db_file: str, *, safe_create: bool = False) -> None:
        self.con = sqlite3.connect(db_file)
        self.cur = self.con.cursor()
        self.schema = ["dhash TEXT"]

        if safe_create:
            self.safe_table_create()

    def safe_table_create(self):
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS entries({','.join(self.schema)})")

    def commit_entry(self, entry: Union[GTSEntry, str]) -> None:
        if type(entry) is GTSEntry:
            entry = str(hash(entry))

        self.cur.execute("INSERT INTO entries VALUES(?)", (entry,))

    def delete_entry(self, entry_hash: str) -> None:
        if type(entry) is GTSEntry:
            entry = str(hash(entry))

        self.cur.execute("DELETE FROM entries WHERE dhash=?", (entry,))

    def retrieve_entry(self, entry_hash: str) -> Optional[Tuple[str, ...]]:
        self.cur.execute("SELECT * FROM entries WHERE dhash=?", (entry_hash,))

        if res := self.cur.fetchall():
            return res[0]
        return None

    def display(self) -> None:
        self.cur.execute("SELECT * FROM entries")
        for idx, entry in enumerate(self.cur.fetchall()):
            print(f"[{idx}]: {entry}")

    def drop_all_entries(self) -> None:
        self.cur.execute("DELETE FROM entries")

    def get_db_entries(self) -> List[Tuple[str, ...]]:
        cur.execute("SELECT * FROM entries")
        return cur.fetchall()

    def cleanup(self) -> None:
        self.con.commit()
        self.con.close()


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

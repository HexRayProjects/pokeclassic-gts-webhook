import time, sqlite3, traceback
import bs4, requests

from typing import List
from cachetools import cached, TTLCache
from src.dbhandler import *
from src.gtsentry import GTSEntry, get_html_entries
from src.webhook import post_webhook
from src.data_formats import discord_format


def main(cur: sqlite3.Cursor, *, testing: bool = False) -> List[GTSEntry]:
    if testing:
        with open("test.html", "r", encoding="utf-8") as file:
            html = file.read()
    else:
        html = requests.get("https://pkmnclassic.net/gts").text

    soup = bs4.BeautifulSoup(html, "html.parser")

    new_entries = []
    db_entries = get_db_entries(cur)
    current_entries = get_html_entries(soup)
    hashed_entries = [*map(str, map(hash, current_entries))]

    for entry in db_entries:
        if entry not in hashed_entries:
            print(f"Deleting entry: {entry}")
            delete_entry(cur, entry)

    for entry, _hash in zip(current_entries, hashed_entries):
        if _hash in db_entries:
            continue

        print(f"Committing entry: {_hash}")
        commit_entry(cur, _hash)
        new_entries.append(entry)

    con.commit()
    return new_entries


def post_entries(entries: List[GTSEntry]) -> None:
    discord_url = "https://discord.com/api/webhooks/1051705794606936134/uJl-xwxPlJafu7HOdpiSjexfnuYS2Hdbib2FZR8nPvpwxPGo1lBAean-eXl4tm5Ty6sQ"

    for entry in entries:
        post_webhook(url=discord_url, data=discord_format(entry), entry=entry)
        time.sleep(3)


if __name__ == "__main__":
    con = sqlite3.connect("entries.db")
    cur = con.cursor()
    safe_table_create(cur)

    try:
        while True:
            try:
                entries = main(cur, testing=False)
                post_entries(entries)
            except requests.exceptions.ConnectionError as e:
                print(f"Connection lost. Trying again in 60 seconds...")
            time.sleep(60)
    except Exception as e:
        print(f"Exception has occurred. Read 'errors.txt' for more detail.")
        traceback.print_exc(file=open("errors.txt", "a"))
    finally:
        con.commit()
        con.close()

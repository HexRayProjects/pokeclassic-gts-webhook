import random, traceback
import requests

from typing import Dict
from .gtsentry import GTSEntry


def post_webhook(*, url: str, data: Dict[str, str], entry: GTSEntry) -> requests.Response:
        res = requests.post(url, json=data)

        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("Error has occurred during post processing. Check 'errors.txt' for details.")
            traceback.print_exc(file=open("errors.txt", "a"))
        else:
            print(f"{res.status_code} | Uploaded entry: {hash(entry)}")

        return res

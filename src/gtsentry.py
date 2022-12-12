import re, hashlib, traceback
import bs4

from typing import List
from dataclasses import dataclass
from .utils import extract_gender


@dataclass
class GTSEntry:
    nickname: str
    species: str
    species_icon: str
    dex_no: str
    nature: str
    held_item: str
    ability: str
    level: str
    gender: str
    ball_name: str
    ball_icon: str
    has_pkrs: bool
    offered_by: str
    wanted_species: str
    wanted_species_icon: str
    wanted_dex_no: str
    wanted_level: str
    wanted_gender: str
    upload_date: str

    def __hash__(self) -> int:
        x = hashlib.md5(
            bytes(
                "".join(str(i) for i in self.__dict__.values()),
                encoding="utf-8"
            )
        ).hexdigest()

        return int(x, 16)

    @staticmethod
    def build(tag: bs4.element.Tag) -> 'GTSEntry':
        td = tag.td
        li_data = tag.td.find_all("li")[1].contents
        tr_data = tag.find_all("tr", {'class': "pfFormPair"})

        has_pkrs = False
        species = td.li.img.get("alt")
        species_icon = f"https://pkmnclassic.net{td.li.img.get('src')}"
        ball_icon = td.find_all("li")[1].img

        if ball_icon is not None:
            ball_name = ball_icon.get("alt")
            ball_icon = f"https://pkmnclassic.net{ball_icon.get('src')}"
        else:
            ball_name = "Poké Ball"
            ball_icon = "https://pkmnclassic.net/images/item-sm/3004.png"

        nickname = tr_data[0].td.contents[0].strip()
        offered_by = tr_data[0].find_all("td")[1].contents[0].strip()

        dex_no = "".join(
            re.findall(
                r'\d+',
                tr_data[1].td.contents[0].split()[1]  # isolate match of "(#number)"
            )
        )   # remove non-numeric characters

        if _ := tr_data[2].td.contents:
            held_item = _[0].get("alt")
        else:
            held_item = "None"

        _ = tr_data[2].find_all("td")[1].contents[1].split()
        wanted_species, wanted_dex_no = " ".join(_[:-1]), _[-1]
        wanted_species_icon = f"https://pkmnclassic.net{tr_data[2].find_all('td')[1].img.get('src')}"
        wanted_dex_no = "".join(re.findall(r'\d+', wanted_dex_no))

        nature = tr_data[3].td.contents[0]
        wanted_gender = extract_gender(tr_data[3].find_all("td")[1].contents[0])
        wanted_level = tr_data[3].find_all("td")[1].contents[0].replace(wanted_gender, "").strip()
        ability = tr_data[4].td.contents[0]
        upload_date = tr_data[4].find_all("td")[1].contents[0]

        if not (span := tag.td.find_all("li")[1].span) is None:
            if span.contents[0] == "PKRS":
                has_pkrs = True

        if len(li_data) == 5:
            gender = extract_gender(li_data[2])
            level = " ".join(li_data[2].replace(gender, "").split()[:2])
        else:
            gender = extract_gender(li_data[-1])
            level = " ".join(li_data[-1].replace(gender, "").split()[:2])

        entry = GTSEntry(
            nickname = nickname,
            species = species,
            species_icon = species_icon,
            dex_no = dex_no,
            nature = nature,
            held_item = held_item,
            ability = ability,
            level = level,
            gender = gender,
            ball_name = ball_name,
            ball_icon = ball_icon,
            has_pkrs = has_pkrs,
            offered_by = offered_by,
            wanted_species = wanted_species,
            wanted_species_icon = wanted_species_icon,
            wanted_dex_no = wanted_dex_no,
            wanted_level = wanted_level,
            wanted_gender = wanted_gender,
            upload_date = upload_date,
        )

        return entry


def get_html_entries(soup: bs4.BeautifulSoup) -> List[GTSEntry]:
    ret = []
    for table in soup.find_all("table", {'class': "gtsPokemonSummary"}):
        try:
            ret.append(GTSEntry.build(table))
        except Exception as e:
            print("Error has occurred during build process. Read 'errors.txt' for details.")
            traceback.print_exc(file=open("errors.txt", "a"))

            with open("tables.txt", "a") as file:
                file.write(str(table))

    return ret

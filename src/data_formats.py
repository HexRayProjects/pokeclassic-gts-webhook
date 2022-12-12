import random

from typing import Dict
from .gtsentry import GTSEntry


def discord_format(entry: GTSEntry) -> Dict[str, str]:
        data = {
            'username': "GTS Updates",
            'url': "https://pkmnclassic.net/gts/",
            'avatar_url': "https://pkmnclassic.net/images/heading-icon.png",
            'embeds': [{
                'title': f"{entry.species} (#{entry.dex_no}){' (PKRS+)' if entry.has_pkrs else ''}",
                'color': random.randint(0x0, 0xffffff),
                'description': f"**Name:** {entry.nickname}\n**Gender:** {entry.gender}\n**Level:** {entry.level}\n**Nature:** {entry.nature}\n**Ability:** {entry.ability}\n**Held Item:** {entry.held_item}\n\n**Date:** {entry.upload_date}",
                'author': {
                    'name': entry.offered_by,
                    'icon_url': entry.ball_icon,
                },
                'footer': {
                    'text': f"Wanted: {entry.wanted_species} (#{entry.wanted_dex_no}) {entry.wanted_gender} @ {entry.wanted_level}",
                    'icon_url': entry.wanted_species_icon
                },
                'image': {
                    'url': entry.species_icon
                }
            }]
        }

        return data

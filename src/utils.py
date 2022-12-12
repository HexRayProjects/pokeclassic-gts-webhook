import re


def extract_gender(data: str) -> str:
    g = re.findall(r'(♂|♀)', data)
    return "" if not g else g[0]

import re


def extract_title(markdown):
    h1 = re.findall(r"^#{1}\s.+$", markdown)
    if len(h1) == 0:
        raise Exception("markdown needs a valid h1 header")

    return " ".join(h1)

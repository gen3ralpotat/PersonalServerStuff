from fuzzywuzzy import process
import os
import tomllib


KEEP_YOUR_VOICE_LOW = "keep your voice low"

TRIGGERS = []
RESPONSES = {}

with open(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "Queries.toml", 'rb') as fp:
    Queries = tomllib.load(fp)
    for query in Queries:
        for trigger in Queries.get(query).get("triggers"):
            TRIGGERS.append(trigger)
            RESPONSES[trigger] = query
    del Queries


def check_for_triggers(string: str):
    """
        Returns message if triggerd,
            or else returns none

    """
    if string.isupper():
        return "Keep your voice low"

    result = process.extractOne(string, TRIGGERS, score_cutoff=90)

    if result:
        return RESPONSES[result[0]]

    return None
